from auth_utils import verify_password, hash_password
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory users dictionary for local testing
USERS = {
    "demo@bank.com": {
        "hashed_password": hash_password("demo123"),
        "name": "Demo User"
    }
}

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
    return jsonify({
        "message": "Welcome to the Banking API",
        "routes": ["/api/login", "/api/register", "/api/balance", "/api/transactions", "/api/fraud-alerts", "/api/health"]
    })


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    user = USERS.get(data.get("username"))
    if user and verify_password(data.get("password"), user["hashed_password"]):
        return jsonify({"token": "real-token", "user": {"name": user["name"]}})
    return jsonify({"error": "Invalid credentials"}), 401


@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if username in USERS:
        return jsonify({"error": "User already exists"}), 400
    USERS[username] = {
        "hashed_password": hash_password(password),
        "name": username
    }
    return jsonify({"message": "Registration successful"})


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
