from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys
import math
import pytz

#to take out
MAX_PEOPLE_READY = 2
MAX_MINUTES_READY = 5
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
    createdAt = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp(), nullable=False)
    readyAt = db.Column(db.TIMESTAMP(timezone=True), nullable=True)

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

@app.route("/queue/event/<int:eid>/waiting-fail", methods=["PUT"])
def check_and_update_fail_status(eid):
    queue_entries = Queue.query.filter(Queue.status == 'Waiting', Queue.eid==eid).all()

    if len(queue_entries) == 0 :
        return jsonify({"code": 200, "message": f"No user status was updated in queue for event {eid}", "updated_entries": []}), 200

    updated_entries = []

    for queue_entry in queue_entries:
        queue_entry.status = 'Fail'
        updated_entries.append({"eid": queue_entry.eid, "uid": queue_entry.uid})

    try:
        db.session.commit()
        return jsonify({"code": 200, "message": "Update to 'Fail' completed successfully.", "updated_entries": updated_entries}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "An error occurred during update. " + str(e)}), 500

@app.route("/queue/event/<int:eid>/ready-missed", methods=["PUT"])
def check_and_update_missed_status(eid):
    fifteen_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=MAX_MINUTES_READY)
    queue_entries = Queue.query.filter(Queue.status == 'Ready', Queue.readyAt <= fifteen_minutes_ago, Queue.eid==eid).all()

    if len(queue_entries) == 0 :
        return jsonify({"code": 200, "message": f"No user status was updated in queue for event {eid}", "updated_entries": []}), 200

    updated_entries = []

    for queue_entry in queue_entries:
        queue_entry.status = 'Missed'
        updated_entries.append({"eid": queue_entry.eid, "uid": queue_entry.uid})

    try:
        db.session.commit()
        return jsonify({"code": 200, "message": "Update to 'Missed' completed successfully.", "updated_entries": updated_entries}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "An error occurred during update. " + str(e)}), 500


@app.route("/queue/event/<int:eid>/waiting-ready", methods=["PUT"])
def update_queue_status_ready(eid):
        data = request.get_json()
        no_of_tickets = data.get("tickets_remaining")
        no_of_ready_in_queue =   Queue.query.filter_by(status='Ready', eid=eid).count()
        queue_entries = Queue.query.order_by(db.asc(Queue.createdAt)).filter_by(status='Waiting', eid=eid).limit(min(no_of_tickets,MAX_PEOPLE_READY)-no_of_ready_in_queue).all()

        if len(queue_entries) ==0 :
            return jsonify({"code": 404, "message": "Number of people ready has reached maximum"}), 404

        updated_entries = []
        try:
            for queue_entry in queue_entries:
                queue_entry.status = "Ready"
                updated_entries.append({
                    "uid" : queue_entry.uid,
                    "eid" : queue_entry.eid
                })
                
            db.session.commit()
            return jsonify({"code": 200, 
                            "message": f"Update to 'Ready' completed successfully for the first {min(no_of_tickets,MAX_PEOPLE_READY)-no_of_ready_in_queue} rows."
                            , "updated_entries": updated_entries}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "message": "An error occurred during bulk update.", "error": str(e)}), 500

#new function for poskitix suggestion
@app.route("/queue/event/<int:eid>/ready-paying", methods=["PUT"])
def paying_queue(eid):
    queue_entries = Queue.query.filter(Queue.status == 'Ready', eid=eid).all()

    updated_entries = []

    for queue_entry in queue_entries:
        queue_entry.status = 'Paying'
        updated_entries.append({"eid": queue_entry.eid, "uid": queue_entry.uid})

    try:
        db.session.commit()
        return jsonify({"code": 200, "message": "Update to 'Paying' completed successfully.", "updated_entries": updated_entries}), 200
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

        queue_entry.status = 'Done'
        db.session.commit()

        queue_entry = Queue.query.filter_by(status='Ready', eid=eid,uid=uid).one()

        return jsonify({"code": 200, "message": f"User {uid} updated to 'Bought' successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

#new function for poskitix suggestion
@app.route("/queue/event/<int:eid>/user/<int:uid>/paying-done", methods=["PUT"])
def update_queue_status_paid(eid,uid):
    try:
        number_of_user_paid = Queue.query.filter_by(status='Paying', eid=eid,uid=uid).count()
        #only either 0 or 1 because eid uid is primary key
        if number_of_user_paid ==0:
            return jsonify({"code": 404, "message": f"User {uid} in event {eid} has not paid."}), 404

        queue_entry = Queue.query.filter_by(status='Paying', eid=eid,uid=uid).one()

        queue_entry.status = 'Done'
        db.session.commit()

        queue_entry = Queue.query.filter_by(status='Paying', eid=eid,uid=uid).one()

        return jsonify({"code": 200, "message": f"User {uid} updated to 'Bought' successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

#poskitix solution paying to missed if exceed 15minutes since readyat time but this is specific to one at a time
@app.route("/queue/event/<int:eid>/user/<int:uid>/paying-missed", methods=["PUT"])
def update_paying_status_to_missed(eid, uid):
    try:
        # Fetch the queue entry for the given eid and uid with 'Paying' status
        queue_entry = Queue.query.filter_by(eid=eid, uid=uid, status='Paying').first()
        
        if queue_entry is None:
            return jsonify({"code": 404, "message": f"No user with uid {uid} in event {eid} found in 'Paying' status."}), 404
        
        # Check if the time difference exceeds 15 minutes between current time and ReadyAt time
        fifteen_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=15)
        if queue_entry.readyAt <= fifteen_minutes_ago:
            # Update the status to 'Missed'
            queue_entry.status = 'Missed'
            db.session.commit()
            return jsonify({"code": 200, "message": f"User {uid} in event {eid} status updated from 'Paying' to 'Missed'."}), 200
        else:
            return jsonify({"code": 400, "message": f"Time limit not exceeded for user {uid} in event {eid} to update status from 'Paying' to 'Missed'."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500


@app.route("/queue/event/<int:eid>/user/<int:uid>")
def find_specific_queue_status(eid, uid):
    output_status = db.session.scalars(db.select(Queue).filter_by(eid=eid, uid=uid).limit(1)).first()
    #what if the user not in queue

    if output_status == None:
        return jsonify({"code": 404, "message": "No queue found."}), 404

    if output_status.status == "Waiting":
        #position = number of people ahead of me who are not ready
        number_people_ahead =1 +  Queue.query.filter(Queue.eid == eid,Queue.status == "Waiting",  Queue.createdAt < output_status.json()["createdAt"]).count()
        position_in_line = 1 + number_people_ahead

        #estimate waiting time

        #step 1 for the people who are ready 
        #consider worst case where the only time people are admitted into "Ready"
        #is when people ready all are cleared i.e. Done/Failed
        ready_user_with_latest_ready_time = Queue.query.filter(Queue.eid == eid, Queue.status == "Ready").order_by(db.desc(Queue.readyAt)).first()
        if ready_user_with_latest_ready_time is not None:
            latest_ready_time = ready_user_with_latest_ready_time.readyAt.replace(tzinfo=pytz.utc)
        else:
            latest_ready_time = datetime.now(timezone.utc)

        #then out of people ahead of me who are waiting
        # assume we all enter in groups of 5 (MAX_PEOPLE_READY)
        # and everyone fails / buys last minute
                                                                                    #why floor? because when its my group's turn I will be ready
        maximum_time_to_process_people_ahead = timedelta(minutes=(MAX_MINUTES_READY * (number_people_ahead // MAX_PEOPLE_READY)))
        predicted_time_user_ready = latest_ready_time + maximum_time_to_process_people_ahead
        print(math.ceil(number_people_ahead / MAX_PEOPLE_READY))
        waiting_time = predicted_time_user_ready - datetime.now(timezone.utc)

        output_json = output_status.json()
        output_json["position"] = position_in_line
        output_json["waiting_time_minutes"]=round(waiting_time.total_seconds() / 60)

    if output_status:
        return jsonify({"code": 200, "data": output_json })
    return jsonify({"code": 404, "message": "User not found in queue."}), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)