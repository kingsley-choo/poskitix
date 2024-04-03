from flask_cors import CORS
from flask import Flask

import requests

app = Flask(__name__)
CORS(app)

#joshie's function, not sure what to put for the route tho
@app.route("/get-details/user/<string:email>", methods=["GET"])
def get_events_to_display(email):

    response_user = requests.get(f"http://user:5001/user/email/{requests.utils.quote(email)}")
    if response_user.status_code not in range(200,300):
        return {"code":404, "data":"user not found"},404
    
    user = response_user.json()
    uid = user["uid"]

    #2. get a response        #1. make a request....
    response_events = requests.get(f"http://event/event")

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
        response_tickets_left = requests.get(f"http://ticket:5003/ticket/event/{input_eid}")

        if response_events.status_code not in range(200,300): # if there is an error with tickets of one event - leave it be 
            event["status"] = "error"
        else:
            response_tickets_left_body = response_tickets_left.json()
    
            event["tickets_left"]= response_tickets_left_body["data"]["tickets_left"] 

        #lets check their status in queue
        response_queue_status = requests.get(f"http://queue:5004/queue/event/{input_eid}/user/{uid}")
        if response_queue_status.status_code not in range(200,300):
            #an error! lets just set the queue_status as None
            event["queue_status"] = None
        else:
            event["queue_status"] = response_queue_status.json()["data"]

        response_ticket = requests.get(f"http://ticket:5003/ticket/event/{input_eid}/user/{uid}")
        if response_ticket.status_code not in range(200,300):
            #an error! lets just set the queue_status as None
            event["ticket"] = None
        else:
            event["ticket"] = response_ticket.json()["message"]       

        
    
    return { "code" : 200, "data" : events, "user" : user}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
