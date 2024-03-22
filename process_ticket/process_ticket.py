from os import environ
from flask_cors import CORS
from flask import Flask, request, jsonify

import requests
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

app = Flask(__name__)
CORS(app)

def email(r, event, s):
    for person in r.json()["updated_entries"]:
                uid = person["uid"]
                r_user = requests.get(f"http://localhost:5001/user/{uid}")
                #step 10 & 11 getting emails of all the users with status changed
                if r_user.status_code //200 != 1:
                    return r_user.text, 404
                    #step 12
                exchange="email"
                body = {
                    "user" : r_user.json()["data"],
                    "event" : event
                }
                channel.exchange_declare(exchange=exchange,
                                    exchange_type='topic', durable=True)
                channel.basic_publish(exchange=exchange,
                                routing_key= s,
                                body=json.dumps(body))

#activity log and error log missing
@app.route("/queue/event/<int:eid>/user/<int:uid>/process")
def process_ticket(eid):
    #step 2 and 3 - get all future events
    r_event = requests.get(f"http://localhost:5002/event")
    if r_event.status_code // 200 != 1:
        return r_event.text, 404
    #step 4 and 5 checking which event still have ticket
    for event in r_event.json()["data"]:
        eid = event["eid"]
        r_ticket = requests.get(f"http://localhost:5003/ticket/event/{eid}")
        if r_ticket.status_code //200 != 1:
            return r_ticket.text, 404
        #step 6 get number of tickets for this event
        tickets_left = r_ticket.json()["data"]["tickets_left"]
        #CASE B - no tickets in this event
        if tickets_left == 0:
            #step 7b & 8 changing status
            r_waitingtofail = requests.get(f"http://localhost:5004/queue/event/{eid}/waiting-fail")
            if r_waitingtofail.status_code // 100 != 2:
                return r_waitingtofail.text, r_waitingtofail.status_code
            #step 9 - returned ID of impacted users in "updated_entries"
            email(r_waitingtofail, event, "waiting.fail")
            # for person in r_waitingtofail.json()["updated_entries"]:
            #     uid = person["uid"]
            #     #step 10 & 11 getting emails of all the users with status changed
            #     r_user = requests.get(f"http://localhost:5001/user/{uid}")
            #     if r_user.status_code //200 != 1:
            #         return r_user.text, 404
            #     #step 12
            #     exchange="email"
            #     body = {
            #         "user" : r_user.json()["data"],
            #         "event" : event
            #     }
            #     channel.exchange_declare(exchange=exchange,
            #                         exchange_type='topic', durable=True)
            #     channel.basic_publish(exchange=exchange,
            #                     routing_key='waiting.fail',
            #                     body=json.dumps(body))
        
        #CASE A - there are still tickets in this event
        else:
            #step 7a & 8 changing status
            r_readytomissed = requests.get(f"http://localhost:5004/queue/event/{eid}/ready-missed")
            if r_readytomissed.status_code // 100 != 2:
                return r_readytomissed.text, r_readytomissed.status_code
            email(r_readytomissed, event, "ready.missed")

            r_waitingtoready = requests.get(f"http://localhost:5004/queue/event/{eid}/waiting-ready/")
            if r_waitingtoready.status_code // 100 != 2:
                return r_waitingtoready.text, r_waitingtoready.status_code
            #step 9 - returned ID of impacted users in "updated_entries"
            email(r_waitingtoready, event, "waiting.ready")
            # for person in r_waitingtoready.json()["updated_entries"]:
            #     uid = person["uid"]
            #     r_user = requests.get(f"http://localhost:5001/user/{uid}")
            #     #step 10 & 11 getting emails of all the users with status changed
            #     if r_user.status_code //200 != 1:
            #         return r_user.text, 404
            #         #step 12
            #     exchange="email"
            #     body = {
            #         "user" : r_user.json()["data"],
            #         "event" : event
            #     }
            #     channel.exchange_declare(exchange=exchange,
            #                         exchange_type='topic', durable=True)
            #     channel.basic_publish(exchange=exchange,
            #                     routing_key='waiting.ready',
            #                     body=json.dumps(body))
    return {
            "status" : 200,}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200, debug=True)