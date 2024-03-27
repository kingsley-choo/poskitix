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
    r = requests.get(f"http://localhost:5004/queue/{eid}/user/{uid}")
    status = r.json()['data']['status']
    if status == 'Ready':
        #invoke payment here
        #pass is supposed to return URL for checkout
        print('payment')
    else:
        return {
            "code" : 400,
            "message" : "Failed to create payment url."
        }, 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5300, debug=True)
