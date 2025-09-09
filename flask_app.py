from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend fetch requests

# Mobitech API details
SMS_API_URL = "https://app.mobitechtechnologies.com/sms/sendsms"
SMS_API_KEY = "cda08a8c58f4d6ae858370d0edba7ee3eda9e2a94e1e48334112de5a32276246"
HEADERS = {
    "h_api_key": SMS_API_KEY,
    "Content-Type": "application/json"
}


@app.route("/")
def home():
    """Serve the SMS form UI."""
    return render_template("index.html")


@app.route("/send-sms", methods=["POST"])
def send_sms():
    """Send SMS to one or more phone numbers."""
    try:
        data = request.get_json()
        mobiles = data.get("mobiles")   # expect a list of numbers
        message = data.get("message")

        if not mobiles or not message:
            return jsonify({"error": "Phone numbers and message are required"}), 400

        results = []
        for mobile in mobiles:
            payload = {
                "mobile": mobile.strip(),
                "response_type": "json",
                "sender_name": "FULL_CIRCLE",  # make sure this sender ID is registered
                "service_id": 0,
                "message": message
            }

            try:
                response = requests.post(SMS_API_URL, headers=HEADERS, json=payload, timeout=15)
                results.append({
                    "mobile": mobile,
                    "status_code": response.status_code,
                    "response": response.json() if response.content else {}
                })
            except Exception as e:
                results.append({
                    "mobile": mobile,
                    "error": str(e)
                })

        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Runs on all interfaces so Codespaces can forward port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
