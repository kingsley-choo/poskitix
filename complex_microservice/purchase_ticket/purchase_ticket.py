from flask import Flask, request, jsonify, redirect, render_template_string
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/purchase_ticket/event/<int:eid>/user/<int:uid>", methods=["POST"])
def purchase_ticket(eid,uid):
    #is the user ready to buy ticket? -> Check user status if it is ready
    r = requests.get(f"http://queue:5004/queue/event/{eid}/user/{uid}")
    queue_status = r.json()["data"]
    print(queue_status)
    if r.status_code not in range(200,300):
        return r.text,r.status_code

    status = queue_status['status']
    print(status)
    if status == 'Ready':
            
        if queue_status["checkout_session_id"] is None:
            #invoke payment here e.g. r_payment_info = requests.get(payment)
            #this is supposed to return URL for checkout and sid
            r_payment_info = requests.post(f"http://payment:5005/create-checkout-session/event/{eid}")
            if r_payment_info.status_code not in range(200,300):
                return {"data" : "failed to create payment link", "code" : 500}, 500
            #r_payment_info.json()[follow schema for uid/eid/sid]
            session = r_payment_info.json()["data"]
            sid = session['id']
            r_update_session_id = requests.put(f"http://queue:5004/queue/event/{eid}/user/{uid}/session_id/{sid}")
            if r_update_session_id.status_code == 200:
                return {"code":200, "data": "Success", "url" : session["url"]}, 200
            else : 
                return {"code": 200, "data" : "Success but not recorded please contact us after paying","url": session.url}, 200
        else:
            r_payment_info = requests.get(f"http://order:5005/order/{queue_status["checkout_session_id"]}/url")
            if r_payment_info.status_code not in range(200,300):
                return {"code":500, "data":"issue with stripe"},500
            
            url = r_payment_info.json()["data"]

            return {"code":200, "data": "Success", "url" : url}, 200
    else:
        return {"code" : 400, "data" : "Ineligible to buy ticket"}



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5300, debug=True)
