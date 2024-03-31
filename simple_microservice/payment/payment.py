from flask import Flask, request, jsonify, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import stripe
import time
import datetime

# This is a public sample test API key.
# Public key
# stripe.api_key = 'pk_test_51OuAKs2M2WNHYrTAAUCTH5EJDq3rYJLBJGMaQi60IcTzQakxpfMsyGI0SFqWt56yjc87EEfskoT4RiYtFaWTn9nF00QMnUPw0Q'

# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
# Secret key
# Henry's API key
stripe.api_key = 'sk_test_51OuAKs2M2WNHYrTASwFcISy1TyhM9f8Vt4X1IaLzZQRQvzTkbGCUXiJk0Fi2O0bEuUwJlAo8851TXMtd8ygPhJhA00kmXWvzBC'

# Joshua's API key
# stripe.api_key = 'sk_test_51OyrMORsQ5WaThPekIN8poryHhxBLzXKQ9EhYDvc58oNPSRTKrgpZy3haLx99TBdFw4ktMD27A7MClQI0SfSeZlz00L4z8Mwqf'


app = Flask(__name__)

#make 2 products one for each event - create separate script

# stripe.Price.create( 
# currency="sgd",
# # unit_amount in cents 
# unit_amount= 1500, 
# lookup_key= "1", 
# product_data={"name" : "Eras Tour"} 
# )

# stripe.Price.create( 
# currency="sgd", 
# # unit_amount in cents
# unit_amount= 3000 , 
# lookup_key= "2", 
# product_data={"name" : "Nathan Tour"} 
# )

YOUR_DOMAIN = environ.get("YOUR_DOMAIN")

def lookup_event(event):
    list_price_result = stripe.Price.list(lookup_keys=[event])
    if not list_price_result:
        return jsonify({"code": 404, "message": "Event not found."}), 404
    print(list_price_result)
    the_price_i_need = list_price_result["data"][0] 
    the_id_i_need = the_price_i_need["id"]
    return the_id_i_need

# Create Checkout Session
@app.route('/create-checkout-session/event/<int:eid>', methods=['POST'])
def create_checkout_session(eid):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # 'price': 'price_1OwTOw2M2WNHYrTAGgU9CBwp',
                    'price': lookup_event(eid),
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url = YOUR_DOMAIN + '/process_payment.html' + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = YOUR_DOMAIN + '/fail.html',

            # Timestamp must be at least 30 minutes
            expires_at = int(time.time() + (60 * 30)), # Configured to expire after 30 minutes
        )
    except Exception as e:
        return str(e)

    session_id = checkout_session.id
    # return redirect(checkout_session.url, code=303)

    return {"code": 201, "data": checkout_session},201



@app.route('/order/<session_id>/payment_status', methods=['GET'])
def order_success(session_id):

    session = stripe.checkout.Session.retrieve(
        session_id
    )   

    if session["payment_status"] == "paid":
        return jsonify({"code": 200, "message": "Payment Successful"}), 200
    else:
        return jsonify({"code": 400, "message": "Payment Failed"}), 400
    
@app.route('/order/<session_id>/expire', methods=['DELETE'])
def expire_session(session_id):

    stripe.checkout.Session.expire(
        session_id
    )   
    return jsonify({"code": 200, "message": "Session Expired"}), 200


@app.route('/order/<session_id>/url', methods=['GET'])
def get_order_url(session_id):
    session = stripe.checkout.Session.retrieve(
        session_id
    )   
    if session.url is None:
        return {"code": 400, "data": "session no longer valid"}, 400

    return {"code" : 200, "data" : session.url}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
