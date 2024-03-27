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

#joshie's function, not sure what to put for the route tho
@app.route("/event/user/<int:uid>", methods=["GET"])
def get_events_to_display(uid):

    #2. get a response        #1. make a request....
    response_events = requests.get(f"http://localhost:5002/event")

    #did it fail? lets check
    if response_events.status_code not in range(200,300):
        return response_events.text,response_events.status_code # REFLECT the result - STOP because cannot proceed without events

    #if it reaches here then the success must have passed
    events_json_body = response_events.json()

    #lets get the events inside
    events = events_json_body["data"]

    # this is how one event looks like
    # {
    #     "eid" : ....,
    #     "event name" : ...,
    # }
    # we want to ADD information i.e. whether user status in queue and ticket remaining

    for event in events:
        input_eid = event["eid"]

        #FIRST, how many tickets are left?
        response_tickets_left = requests.get(f"http://localhost:5003/ticket/event/{input_eid}")

        if response_events.status_code not in range(200,300): # if there is an error with tickets of one event - leave it be 
            event["status"] = "error"

        response_tickets_left_body = response_tickets_left.json()

        #oh no more, so we can conclude they probably not in queue
        if response_tickets_left_body["data"]["tickets_left"] == 0:
            event["sold_out"] = True
            event["queue_status"] = None
        #lets check their status in queue
        else:
            event["sold_out"]=False
            #lets check their status in queue
            response_queue_status = requests.get(f"http://localhost:5004/queue/event/{input_eid}/user/{uid}")
            if response_queue_status.status_code not in range(200,300):
                #an error! lets just set the queue_status as None
                event["queue_status"] = None
            else:
                event["queue_status"] = response_queue_status.json()["data"]
    
    return { "code" : 200, "data" : events}


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
        "data" : "success"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
