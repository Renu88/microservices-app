from flask import Flask, jsonify
import socket
import requests
import os

app = Flask(__name__)

GREETING_SERVICE_URL = os.environ.get("GREETING_SERVICE_URL", "http://localhost:5000")

@app.route("/")
def home():
    return jsonify({
        "service": "order-service",
        "message": "order-service is running",
        "hostname": socket.gethostname()
    })

@app.route("/create-order")
def create_order():
    try:
        response = requests.get(f"{GREETING_SERVICE_URL}/", timeout=3)
        greeting_data = response.json()
        return jsonify({
            "order_id": "ORD-1001",
            "status": "created",
            "greeting_from": greeting_data
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "order_id": "ORD-1001",
            "status": "failed",
            "error": str(e)
        }), 503

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
