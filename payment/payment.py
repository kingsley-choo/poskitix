from flask import Flask, request, jsonify, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys
import stripe
import time

# This is a public sample test API key.
# Public key
# stripe.api_key = 'pk_test_51OuAKs2M2WNHYrTAAUCTH5EJDq3rYJLBJGMaQi60IcTzQakxpfMsyGI0SFqWt56yjc87EEfskoT4RiYtFaWTn9nF00QMnUPw0Q'

# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
# Secret key
stripe.api_key = 'sk_test_51OuAKs2M2WNHYrTASwFcISy1TyhM9f8Vt4X1IaLzZQRQvzTkbGCUXiJk0Fi2O0bEuUwJlAo8851TXMtd8ygPhJhA00kmXWvzBC'


app = Flask(__name__,
            static_url_path='',
            static_folder='public')

app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:root@localhost:3306/book"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)

CORS(app)

YOUR_DOMAIN = 'http://localhost:5000'

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

# Create Checkout Session
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OwTOw2M2WNHYrTAGgU9CBwp',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url = YOUR_DOMAIN + '/success.html' + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = YOUR_DOMAIN + '/cancel.html',
            # How to retreive customer's id here?
            # customer = User.uid,

            # Timestamp must be at least 30 minutes
            expires_at = int(time.time() + (60 * 30)), # Configured to expire after 30 minutes
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route('/order/success', methods=['GET'])
def order_success():
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
  customer = stripe.Customer.retrieve(session.customer)
  expire = stripe.checkout.Session.expire(
  "cs_test_a1Ae6ClgOkjygKwrf9B3L6ITtUuZW4Xx9FivL6DZYoYFdfAefQxsYpJJd3",
)

# To retrieve checkout session's line items? Should this be placed earlier?
# Is this even necessary?  
#   line_items = stripe.checkout.Session.list_line_items(
#   "cs_test_a1enSAC01IA3Ps2vL32mNoWKMCNmmfUGTeEeHXI5tLCvyFNGsdG2UNA7mr",
# )

  return render_template_string('<html><body><h1>Thanks for your order, {{customer.name}}!</h1></body></html>', customer=customer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
