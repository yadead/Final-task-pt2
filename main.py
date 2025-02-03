from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
from userManagement import diary_entry, sdevname, sprojname, allentries, sCHOICEID, get_user_entries, delete_entry, signup, signin
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)

# Set up logging
app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Routes
@app.route("/signup", methods=["POST"])
def signup_route():
    data = request.get_json()
    print("Received data:", data)
    username = data["username"]
    password = data["password"]
    signup(username, password)
    return jsonify({"message": f"User '{username}' signed up successfully!"}), 201

@app.route("/signin", methods=["POST"])
def signin_route():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    if signin(username, password):
        return jsonify({"message": f"{username} has been logged in"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route("/diary/create", methods=["POST"])
def create_entry():
    data = request.get_json()
    Developer = data["developer"]
    Project = data["project"]
    Start_Time = data["start_time"]
    End_Time = data["end_time"]
    Repo = data["repo"]
    Developer_Notes = data["developer_notes"]
    new_id = diary_entry(Developer, Project, Start_Time, End_Time, Repo, Developer_Notes)
    return jsonify({"message": "Diary entry added", "entry_id": new_id}), 201

@app.route("/", methods=["GET"])
@csp_header({
    "base-uri": "'self'",
    "default-src": "'self'",
    "style-src": "'self'",
    "script-src": "'self'",
    "img-src": "'self' data:",
    "media-src": "'self'",
    "font-src": "'self'",
    "object-src": "'self'",
    "child-src": "'self'",
    "connect-src": "'self'",
    "worker-src": "'self'",
    "report-uri": "/csp_report",
    "frame-ancestors": "'none'",
    "form-action": "'self'",
    "frame-src": "'none'",
})
def index():
    return render_template("index.html")

# Error handling if routes or other parts of the code are misconfigured
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # You can change the port if necessary
