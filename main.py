# main.py
from flask import Flask, jsonify, request, session

app = Flask(__name__)

# Needed so Flask can use sessions (for login)
app.config["SECRET_KEY"] = "dev-secret-key-change-later"

# Temporary in-memory "database"
USERS = {
    "alice": "password123",
    "admin": "admin456",
}

@app.route("/")
def root():
    """
    Root endpoint to check API health.
    """
    return jsonify({"status": "ok", "version": "1.0.0"})


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    """
    Simple logic function to test mathematics.
    """
    return jsonify({"result": a + b})


@app.route("/login", methods=["POST"])
def login():
    """
    Simple login using a temporary in-memory database.
    Stores the logged-in user in the Flask session.
    """
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    # Missing fields
    if not username or not password:
        return jsonify({"detail": "Missing username or password"}), 400

    # Check "database"
    if USERS.get(username) != password:
        return jsonify({"detail": "Invalid credentials"}), 401

    # Store user in session
    session["user"] = username
    return jsonify({"message": "Login successful", "user": username}), 200


@app.route("/subtract/<int:a>/<int:b>")
def subtract(a, b):
    """
    Subtract endpoint that can ONLY be used after login.
    """
    if "user" not in session:
        # Not logged in
        return jsonify({"detail": "Authentication required"}), 401

    return jsonify({"result": a - b})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
