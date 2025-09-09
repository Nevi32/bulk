from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # allow requests from any frontend (React, HTML, etc.)

API_URL = "https://app.mobitechtechnologies.com/sms/sendsms"
API_KEY = "cda08a8c58f4d6ae858370d0edba7ee3eda9e2a94e1e48334112de5a32276246"

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "SMS API is running"})

@app.route("/send-sms", methods=["POST"])
def send_sms():
    try:
        data = request.json
        mobiles = data.get("mobiles", [])
        message = data.get("message", "")

        if not mobiles or not message:
            return jsonify({"error": "mobiles and message are required"}), 400

        results = []
        for mobile in mobiles:
            payload = {
                "mobile": mobile,
                "response_type": "json",
                "sender_name": "FULL_CIRCLE",
                "service_id": 0,
                "message": message
            }
            headers = {
                "h_api_key": API_KEY,
                "Content-Type": "application/json"
            }

            try:
                resp = requests.post(API_URL, json=payload, headers=headers, timeout=15)
                results.append({"mobile": mobile, "response": resp.json()})
            except Exception as e:
                results.append({"mobile": mobile, "error": str(e)})

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
