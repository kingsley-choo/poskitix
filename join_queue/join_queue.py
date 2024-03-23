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

@app.route("/?", methods=["GET"])
#joshie's function, not sure what to put for the route tho
def get_events_to_display(uid):
    r_events = request.get(f"http://localhost:5002/event")["data"]

    for event in r_events:
        input_eid = event["eid"]
        r_tickets_left = request.get(f"http://localhost:5003/ticket/event/{input_eid}")["data"]["tickets"]

        if r_tickets_left == 0:
            event["status"] = "Sold Out"

        else:
            #paiseh not sure whats the output so i put "status" correct if im wrong
            r_status = request.get(f"http://localhost:5004/queue/event/{input_eid}/user/{uid}")["data"]["status"]


#activity log and error log missing
@app.route("/queue/event/<int:eid>/user/<int:uid>/join", methods=["POST"])
def join_queue(eid,uid):
    #step 4 and 5 - does the event exist? 
    r_event = requests.get(f"http://localhost:5002/event/{eid}")
    if r_event.status_code // 200 != 1:
        return r_event.text, 404
    #step 6 and 7 - is there still tickets in the event?
    r = requests.get(f"http://localhost:5003/ticket/event/{eid}")
    if r.status_code //200 != 1:
        return r.text, 404
    #step 10 and 11 - does this user exist?
    r_user = requests.get(f"http://localhost:5001/user/{uid}")
    if r_user.status_code // 100 != 2:
        return r_user.text, r_user.status_code
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
