from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

USER = {"username": "demo@bank.com",
        "password": "demo123", "token": "fake-jwt-token"}
BALANCE = {"account": "XXXX-4321", "available": 125000.50, "currency": "INR"}
TRANSACTIONS = [
    {"id": 1, "date": "2025-08-15", "desc": "UPI - Grocery", "amount": -2450.0},
    {"id": 2, "date": "2025-08-16", "desc": "Salary Credit", "amount": 85000.0},
    {"id": 3, "date": "2025-08-20", "desc": "Online Purchase", "amount": -12000.0},
    {"id": 4, "date": "2025-08-29", "desc": "ATM Withdrawal", "amount": -10000.0},
    {"id": 5, "date": "2025-08-30", "desc": "Fund Transfer", "amount": -65000.0},
]

THRESHOLD = 50000.0


@app.get("/api")
def api_root():
    # New route to handle /api directly
    return jsonify({
        "message": "Welcome to the Banking API",
        "routes": ["/api/login", "/api/balance", "/api/transactions", "/api/fraud-alerts", "/api/health"]
    })


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    if data.get("username") == USER["username"] and data.get("password") == USER["password"]:
        return jsonify({"token": USER["token"], "user": {"name": "Demo User"}})
    return jsonify({"error": "Invalid credentials"}), 401


@app.get("/api/balance")
def balance():
    return jsonify(BALANCE)


@app.get("/api/transactions")
def transactions():
    return jsonify({"items": TRANSACTIONS})


@app.get("/api/fraud-alerts")
def fraud_alerts():
    alerts = []
    for tx in TRANSACTIONS:
        if tx["amount"] < 0 and abs(tx["amount"]) >= THRESHOLD:
            alerts.append({
                "transaction_id": tx["id"],
                "reason": f"Large debit >= {THRESHOLD}",
                "amount": tx["amount"],
                "date": tx["date"],
                "desc": tx["desc"]
            })
    return jsonify({"alerts": alerts})


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
