from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys

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

    uid = db.Column(db.int, primary_key=True)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
