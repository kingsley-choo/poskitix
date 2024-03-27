from flask import Flask, request, jsonify, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys
import stripe
import requests
import pika
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:root@localhost:3306/book"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)

CORS(app)

@app.route("/purchase_ticket/event/<int:eid>/user/<int:uid>")
def purchase_ticket(eid,uid):
    #is the user ready to buy ticket? -> Check user status if it is ready
    r = requests.get(f"http://localhost:5004/queue/event/{eid}/user/{uid}")
    status = r.json()['data']['status']
    if status == 'Ready':
        #invoke payment here e.g. r_payment_info = requests.get(payment)
        #this is supposed to return URL for checkout and sid
        print('payment')
        #r_payment_info.json()[follow schema for uid/eid/sid]
        sid = 12345 #example sid for now
        r_update_session_id = requests.put(f"http://localhost:5004/queue/event/{eid}/user/{uid}/session_id/{sid}")
        if r_update_session_id.status_code == 200:
            return {"code":200, "data": "Success"}, 200
    else:
        return {
            "code" : 400,
            "message" : "Failed to create payment url."
        }, 400






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5300, debug=True)
