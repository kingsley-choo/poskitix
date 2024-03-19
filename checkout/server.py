#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request, render_template_string

import stripe
# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
stripe.api_key = 'sk_test_51OuAKs2M2WNHYrTASwFcISy1TyhM9f8Vt4X1IaLzZQRQvzTkbGCUXiJk0Fi2O0bEuUwJlAo8851TXMtd8ygPhJhA00kmXWvzBC'
# stripe.api_key = 'pk_test_51OuAKs2M2WNHYrTAAUCTH5EJDq3rYJLBJGMaQi60IcTzQakxpfMsyGI0SFqWt56yjc87EEfskoT4RiYtFaWTn9nF00QMnUPw0Q'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

# @app.route('/')
# def index():
#     return "Hello, World!"

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OvOba2M2WNHYrTA9cxKUhNh',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html' + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route('/order/success', methods=['GET'])
def order_success():
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
  customer = stripe.Customer.retrieve(session.customer)

  return render_template_string('<html><body><h1>Thanks for your order, {{customer.name}}!</h1></body></html>', customer=customer)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4242, debug=True)