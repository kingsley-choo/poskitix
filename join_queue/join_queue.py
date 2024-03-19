from os import environ
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/queue/event/<int:eid>/join", methods=["POST"])
def join_queue(eid):
    #step 4 and 5
    r = request.get(f"http://queue:5004/event/{eid}")
    if r.status_code == 404:
        return r.text, 404
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
