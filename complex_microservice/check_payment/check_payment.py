from flask import Flask
from flask_cors import CORS
import requests
import pika
import json
from os import environ

connection = pika.BlockingConnection(pika.ConnectionParameters(environ.get("RABBIT_URL"),heartbeat=600,
                                       blocked_connection_timeout=300))
channel = connection.channel()
app = Flask(__name__)

CORS(app)

@app.route("/check_payment/<string:id>", methods= ['POST'])
def check_payment(id):
    #fetch user details based on this checkout id
    r_queue_details = requests.get(f"http://queue:5004/queue/checkout-session-id/{id}")
    if r_queue_details.status_code not in range(200,300):
        return {"code": 404, "data": "user information not found"}, 404
    print(r_queue_details.text)
    #get request from invoking payment microservice if they have paid or not
    #use parameter id here(?)
    r_paid = requests.get(f"http://payment:5005/order/{id}/payment_status")
    #if yes continue
    if r_paid.status_code not in range(200,300):
        return {"code": 400, "data": "payment not completed or link expired"}, 400
    
    #create new ticket for this person will return ticket details if 201
    r_createticket = requests.post(f"http://ticket:5003/ticket", json=r_queue_details.json()["data"])
    print(r_createticket.text)
    eid = r_createticket.json()['message']['eid']
    uid = r_createticket.json()['message']['uid']
    #changing status of this person for this event to done
    r_changestatustodone = requests.put(f"http://queue:5004/queue/event/{eid}/user/{uid}/ready-done")
    #check if change in status was successful
    if r_changestatustodone.status_code //100 != 2:
        return r_changestatustodone.text, r_changestatustodone.status_code

    r_user = requests.get(f"http://user:5001/user/{uid}")
    if r_user.status_code // 100 != 2:
        return {"code":200, "data": "Success but notification not sent"}, 200
    
    r_event = requests.get(f"http://event/event/{eid}")
    if r_event.status_code // 100 != 2:
        return {"code":200, "data": "Success but notification not sent"}, 200   
    print(r_createticket.text)
    exchange="email"
    body = {
        "user" : r_user.json(),
        "event" : r_event.json()["data"],
        "ticket" : r_createticket.json()["message"]
    }
    channel.exchange_declare(exchange=exchange,
                         exchange_type='topic', durable=True)
    channel.basic_publish(exchange=exchange,
                      routing_key='ready.done',
                      body=json.dumps(body))
    return {
        "status" : 200,
        "data" : "success"
    }



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5400, debug=True)