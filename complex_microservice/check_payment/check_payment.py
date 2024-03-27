from flask import Flask, jsonify, redirect, render_template_string
from flask_cors import CORS
import requests
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
app = Flask(__name__)

CORS(app)

@app.route("/check_payment/<string:id>", methods= ['POST'])
def check_payment(id):
    #get request from invoking payment microservice if they have paid or not
    #use parameter id here(?)
    r_paid = requests.get()
    #if yes continue
    #create new ticket for this person will return ticket details if 201
    r_createticket = requests.post(f"http://localhost:5003/ticket", json=r_paid.json())
    eid = r_createticket.json()['message']['eid']
    uid = r_createticket.json()['message']['uid']
    #changing status of this person for this event to done
    r_changestatustodone = requests.put(f"http://localhost:5004/queue/event/{eid}/user/{uid}/ready-done")
    #check if change in status was successful
    if r_changestatustodone.status_code //100 != 2:
        return r_changestatustodone.text, r_changestatustodone.status_code

    r_user = requests.get(f"http://localhost:5001/user/{uid}")
    if r_user.status_code // 100 != 2:
        return {"code":200, "data": "Success but notification not sent"}, 200
    
    r_event = requests.get(f"http://localhost:5002/event/{eid}")
    if r_event.status_code // 100 != 2:
        return {"code":200, "data": "Success but notification not sent"}, 200

    exchange="email"
    body = {
        "user" : r_user.json(),
        "event" : r_event.json(),
        "ticket" : r_createticket.json()
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