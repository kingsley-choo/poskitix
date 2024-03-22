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


class User(db.Model):
    __tablename__ = "user"

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def __init__(self, uid, username, email):
        self.uid = uid
        self.username = username
        self.email = email

    def json(self):
        return {
            "uid": self.uid,
            "username": self.username,
            "email": self.email,
        }

@app.route("/user/<string:email>")
def find_by_email(email):
    output_uid = db.session.scalars(db.select(User).filter_by(email=email).limit(1)).first()

    if output_uid:
        return jsonify({"code": 200, "data": output_uid.json()})
    return jsonify({"code": 404, "message": "User not found."}), 404

@app.route("/queue/payment/<int:eid>/user/<int:uid>")
def purchase_ticket(eid, uid):
    r_status = request.get(f"http://localhost:5004/{eid}/user/{uid}")


#activity log and error log missing
@app.route("/order/success", methods=["GET"])
def process_payment():
    #step 2 and 3 - get all future payments
    r_payment = requests.get(f"http://localhost:4242/success.html")
    if r_payment.status_code // 200 != 1:
        return r_payment.text, 404
    return {"status" : 200}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
