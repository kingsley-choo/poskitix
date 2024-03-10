from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys

#import date
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:@localhost:3306/event"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)

CORS(app)


class Event(db.Model):
    __tablename__ = "event"

    eid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    eventname = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


    def __init__(self, eid, eventname, date, location, description, capacity, price):
        self.eid = eid
        self.eventname = eventname
        self.date = date
        self.location = location
        self.description = description
        self.capacity = capacity
        self.price = price

    def json(self):
        return {
            "eid": self.eid,
            "eventname": self.eventname,
            "date": self.date,
            "location": self.location,
            "description": self.description,
            "capacity": self.capacity,
            "price": self.price
        }

@app.route("/event/<int:eid>")
def find_by_eid(eid):
    output_event = db.session.scalars(db.select(Event).filter_by(eid=eid).limit(1)).first()

    if output_event:
        return jsonify({"code": 200, "data": output_event.json()})
    return jsonify({"code": 404, "message": "Event not found."}), 404

@app.route("/event")
def find_future_events():
    output_events = datetime.now()
    print(output_events)
    # output_events = db.session.scalars(db.select(Event).filter_by(date>date))

    if output_events:
        return 
        # return jsonify({"code": 200, "data": output_events.json()})
    return jsonify({"code": 404, "message": "Event not found."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
