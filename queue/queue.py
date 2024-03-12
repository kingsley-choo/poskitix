from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:root@localhost:3306/queue"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)

CORS(app)


class Queue(db.Model):
    __tablename__ = "queue"

    eid = db.Column(db.int, primary_key=True)
    uid = db.Column(db.int, primary_key=True)
    status = db.Column(db.String(255))
    CreatedAt = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    readyAt = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, eid, uid, status, CreatedAt, ReadyAt= None):
        self.eid = eid
        self.uid = uid
        self.status = status
        self.Created = CreatedAt
        self.ReadyAt = ReadyAt

    def json(self):
        return {
            "eid": self.eid,
            "uid": self.uid,
            "status": self.status,
            "CreatedAt": self.CreatedAt,
            "ReadyAt": self.ReadyAt,
        }



@app.route("/queue", methods = ["POST"])
def create_queue():
    data = request.get_json()

    eid = data.get("eid")
    uid = data.get("uid")
    status = data.get("status", "Waiting")

    if eid is None or uid is None:
        return jsonify(
            {
                "code": 400,
                "message": "Missing required parameters."
            }
            ), 400
    new_queue = Queue(eid=eid, uid=uid, status=status)

    try:
        db.session.add(new_queue)
        db.session.commit()
        return jsonify({"code": 201, "message": "Queue created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the queue. " + str(e)
             }
             ), 500

@app.route("/update_queue_status_ready", methods=["PUT"])
def update_queue_status_ready():
    queue_entries = Queue.query.limit(10).all()

    if not queue_entries:
        return jsonify({"code": 404, "message": "No queue entries found."}), 404

    try:
        for queue_entry in queue_entries:
            queue_entry.status = "ready"
            queue_entry.ReadyAt = datetime.now()

        db.session.commit()
        return jsonify({"code": 200, "message": "Update to 'Ready' completed successfully for the first 10 rows."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "An error occurred during bulk update.", "error": str(e)}), 500

@app.route("/check_and_update_missed_status", methods=["PUT"])
def check_and_update_missed_status():
    fifteen_minutes_ago = datetime.now() - timedelta(minutes=15)
    queue_entries = Queue.query.filter(Queue.status == 'Ready', Queue.readyAt <= fifteen_minutes_ago).all()

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

@app.route("/update_queue_status_bought", methods=["PUT"])
def update_queue_status_bought():
    try:
        ready_queue_entries = Queue.query.filter_by(status='Ready').all()

        updated_entries = []

        for queue_entry in ready_queue_entries:
            queue_entry.status = 'Bought'
            updated_entries.append({"eid": queue_entry.eid, "uid": queue_entry.uid})

        db.session.commit()

        return jsonify({"code": 200, "message": "Queue statuses updated to 'Bought' successfully.", "updated_entries": updated_entries}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/find_specific_queue_status/<int:eid>/<int:uid>")
def find_specific_queue_status(eid, uid):
    output_status = db.session.scalars(db.select(Queue).filter_by(eid=eid, uid=uid).limit(1)).first()

    if output_status:
        return jsonify({"code": 200, "data": output_status.json()})
    return jsonify({"code": 404, "message": "Queue not found."}), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200, debug=True)
