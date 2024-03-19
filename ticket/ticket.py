from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys
import uuid

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:example@localhost:3306/ticket"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)

CORS(app)


# class User(db.Model):
#     __tablename__ = "user"

#     uid = db.Column(db.int, primary_key=True)
#     username = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), nullable=False)

#     def __init__(self, uid, username, email):
#         self.uid = uid
#         self.username = username
#         self.email = email

#     def json(self):
#         return {
#             "uid": self.uid,
#             "username": self.username,
#             "email": self.email,
#         }

class Ticket(db.Model):
    __tablename__ = "ticket"
    tid = db.Column(db.String(255))
    eid = db.Column(db.ForeignKey(
        'ticket_event.eid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)

    def __init__(self, eid, uid,tid):
        self.eid = eid
        self.uid = uid
        self.tid = tid
        
    def json(self):
        return {
            "eid": self.eid,
            "uid": self.uid,
            "tid": self.tid,
        }

class Ticket_Event(db.Model):
    __tablename__ = "ticket_event"
    eid = db.Column(db.Integer, primary_key=True)
    tickets_left = db.Column(db.Integer)

    def __init__(self, eid, ticket_left):
        self.eid = eid
        self.tickets_left = tickets_left
        
    def json(self):
        return {
            "eid": self.eid,
            "tickets_left": self.tickets_left,
        }

#create new ticket
@app.route("/ticket", methods = ["POST"])
def create_ticket():
    data = request.get_json()

    eid = data.get("eid")
    uid = data.get("uid")

    if eid is None or uid is None:
        return jsonify(
            {
                "code": 400,
                "message": "Missing required parameters."
            }
            ), 400
    new_ticket = Ticket(eid=eid, uid=uid, tid= str(uuid.uuid1()))

    try:
        db.session.add(new_ticket)
        db.session.commit()
        return jsonify({"code": 201, "message": "Ticket created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the ticket. " + str(e)
             }
             ), 500
             

#get number of tickets left from db with eid
@app.route("/ticket_event/<int:eid>")
def get_ticket_left(eid):
    output= db.session.scalars(db.select(Ticket_Event).filter_by(eid=eid).limit(1)).first()
    
    if not output:
        return jsonify({"code": 404, "message": "Event not found."}), 404
    
    if output.tickets_left >0:
        return jsonify(
            {
                "code": 200,
                "data": output.json()
            }
            )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Oh no! Event is SOLD OUT."
            }
            ), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
