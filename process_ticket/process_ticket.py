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

#activity log and error log missing
@app.route("/queue/event/<int:eid>/user/<int:uid>/process", methods=[["GET"],["PUT"]])
def process_ticket(eid,uid):
    #step 2 and 3 - get all future events
    r_event = requests.get(f"http://localhost:5002/event")
    if r_event.status_code // 200 != 1:
        return r_event.text, 404
    #step 4, 5, and 6 - check which event still have tickets & get number of tickets for each event
    for event in r_event.json()["data"]:
        eid = event["eid"]
        r_ticket = requests.get(f"http://localhost:5003/ticket/event/{eid}")
        if r_ticket.status_code //200 != 1:
            continue

        if r_ticket == 0:
            r = requests.get(f"http://localhost:5004/queue/event/{eid}/waiting-fail")
            if r.status_code // 100 != 2:
                return r.text, r.status_code
            
        else:
            r = requests.get(f"http://localhost:5004/queue/event/{eid}/waiting-ready/")

            if r.status_code // 100 != 2:
                return r.text, r.status_code
            
        for person in r_ticket.json()["data"]:
            uid = person["uid"]
            r_user = requests.get(f"http://localhost:5001/user/{uid}")
            if r_user.status_code //200 != 1:
                return r_user.text, 404
            exchange="email"
            body = {
                "user" : r_user.json()["data"],
                "event" : event.json()["data"]
            }
            channel.exchange_declare(exchange=exchange,
                                exchange_type='topic', durable=True)
            channel.basic_publish(exchange=exchange,
                            routing_key='waiting.fail',
                            body=json.dumps(body))
            return {
                "status" : 200,
                "data" : "success join queue"
            }



    #step 7 and 8 - change (maximum no. of users) status waiting-ready
    r = requests.get(f"http://localhost:5004/queue/event/{eid}/waiting-ready/")
    if r.status_code // 100 != 2:
        return r.text, r.status_code
    #step 8 and 9 - please let this user join
    r = requests.post(f"http://localhost:5004/queue", json= {
        "eid" : eid,
        "uid" :uid
    })  
    if r.status_code // 100 != 2:

        return r.text, r.status_code
    #step 12
    exchange="email"
    body = {
        "user" : r_user.json()["data"],
        "event" : r_event.json()["data"]
    }
    channel.exchange_declare(exchange=exchange,
                         exchange_type='topic', durable=True)
    channel.basic_publish(exchange=exchange,
                      routing_key='waiting',
                      body=json.dumps(body))
    return {
        "status" : 200,
        "data" : "success join queue"
    }

    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)