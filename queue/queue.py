from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys

#to take out
MAX_PEOPLE_READY = 2
MAX_MINUTES_IN_QUEUE = 5
##max in queue is 15 minutes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:example@localhost:3306/queue"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)



CORS(app)


class Queue(db.Model):
    __tablename__ = "queue"

    eid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    createdAt = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    readyAt = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, eid, uid, status="Waiting"):
        self.eid = eid
        self.uid = uid
        self.status = status

    def json(self):
        return {
            "eid": self.eid,
            "uid": self.uid,
            "status": self.status,
            "createdAt": self.createdAt,
            "readyAt": self.readyAt,
        }



@app.route("/queue", methods = ["POST"])
def create_queue():
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
    new_queue = Queue(eid=eid, uid=uid)

    try:
        db.session.add(new_queue)
        db.session.commit()
        return jsonify({"code": 201, "message": f"User {uid} entered queue created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the queue. " + str(e)
             }
             ), 500

@app.route("/queue/event/<int:eid>/waiting-ready", methods=["PUT"])
def update_queue_status_ready(eid):
        data = request.get_json()
        no_of_tickets = data.get("tickets_remaining")
        no_of_ready_in_queue =   Queue.query.filter_by(status='Ready', eid=eid).count()
        queue_entries = Queue.query.order_by(db.asc(Queue.createdAt)).filter_by(status='Waiting', eid=eid).limit(min(no_of_tickets,MAX_PEOPLE_READY)-no_of_ready_in_queue).all()

        if len(queue_entries) ==0 :
            return jsonify({"code": 404, "message": "Number of people ready has reached maximum"}), 404

        result = []
        try:
            for queue_entry in queue_entries:
                queue_entry.status = "Ready"
                result.append({
                    "uid" : queue_entry.uid,
                    "eid" : queue_entry.eid
                })
                
            db.session.commit()
            return jsonify({"code": 200, 
                            "message": f"Update to 'Ready' completed successfully for the first {min(no_of_tickets,MAX_PEOPLE_READY)-no_of_ready_in_queue} rows."
                            , "update_entries": result}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "message": "An error occurred during bulk update.", "error": str(e)}), 500



@app.route("/queue/event/<int:eid>/ready-missed", methods=["PUT"])
def check_and_update_missed_status(eid):
    fifteen_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=MAX_MINUTES_IN_QUEUE)
    queue_entries = Queue.query.filter(Queue.status == 'Ready', Queue.readyAt <= fifteen_minutes_ago, Queue.eid==eid).all()

    if len(queue_entries) == 0 :
        return jsonify({"code": 200, "message": f"No user status was updated in queue for event {eid}", "updated_entries": []}), 200

    updated_entries = []

    for queue_entry in queue_entries:
        queue_entry.status = 'missed'
        updated_entries.append({"eid": queue_entry.eid, "uid": queue_entry.uid})

    try:
        db.session.commit()
        return jsonify({"code": 200, "message": "Update to 'Missed' completed successfully.", "updated_entries": updated_entries}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "An error occurred during update. " + str(e)}), 500
    
@app.route("/queue/event/<int:eid>/waiting-fail", methods=["PUT"])
def close_queue(eid):
    queue_entries = Queue.query.filter(Queue.status == 'Waiting').all()

    updated_entries = []

    for queue_entry in queue_entries:
        queue_entry.status = 'fail'
        updated_entries.append({"eid": queue_entry.eid, "uid": queue_entry.uid})

    try:
        db.session.commit()
        return jsonify({"code": 200, "message": "Update to 'Missed' completed successfully.", "updated_entries": updated_entries}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "An error occurred during update. " + str(e)}), 500


@app.route("/queue/event/<int:eid>/user/<int:uid>/ready-done", methods=["PUT"])
def update_queue_status_bought(eid,uid):
    try:
        number_of_user_ready = Queue.query.filter_by(status='Ready', eid=eid,uid=uid).count()
        #only either 0 or 1 because eid uid is primary key
        if number_of_user_ready ==0:
            return jsonify({"code": 404, "message": f"User {uid} in event {eid} is not in queue/not ready"}), 404

        queue_entry = Queue.query.filter_by(status='Ready', eid=eid,uid=uid).one()

        queue_entry.status = 'Bought'
        db.session.commit()

        queue_entry = Queue.query.filter_by(status='Ready', eid=eid,uid=uid).one()

        return jsonify({"code": 200, "message": f"User {uid} updated to 'Bought' successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/queue/event/<int:eid>/user/<int:uid>")
def find_specific_queue_status(eid, uid):
    output_status = db.session.scalars(db.select(Queue).filter_by(eid=eid, uid=uid).limit(1)).first()

    if output_status:
        return jsonify({"code": 200, "data": output_status.json()})
    return jsonify({"code": 404, "message": "User not found in queue."}), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
