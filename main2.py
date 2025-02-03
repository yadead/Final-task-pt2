from userManagement import diary_entry, sdevname, sprojname, allentries, sCHOICEID, get_user_entries, delete_entry, signup, signin
from flask import request, jsonify, redirect, url_for, session
from datetime import datetime
from flask import Flask


app = Flask(__name__)

#prompt user for username and passwordFto sign up with
@app.route("/signup", methods=["POST"])
def signup_route():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    signup(username, password)
    return jsonify({"message": f"User '{username}' signed up successfully!"}), 201


#prompt user for username and password to sign in with
@app.route("/signin", methods=["POST"])
def signin_route():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if signin(username, password):
        session['username'] = username
        return jsonify({"message": f"{username} has been logged in"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401




# query user for information about diary entry
@app.route("/diary/create", methods=["POST"])
def create_entry():
    data = request.get_json()
    Developer = data["developer"]
    Project = data["project"]
    Start_Time = data["start_time"]
    End_Time = data["end_time"]
    time_format = "%H:%M %d/%m/%Y"
    start_dt = datetime.strptime(Start_Time, time_format)
    end_dt = datetime.strptime(End_Time, time_format)
    Time_Worked = end_dt - start_dt
    total_minutes = Time_Worked.total_seconds() / 60
    rounded_minutes = math.ceil(total_minutes / 15) * 15
    rounded_hours = rounded_minutes / 60
    Time_Worked = rounded_hours
    now = datetime.now()
    Diary_Entry = now.strftime("%H:%M %d/%B/%Y")
    new_id = diary_entry(Developer, Project, Start_Time, End_Time, Diary_Entry, Time_Worked, Repo, Developer_Notes)
    Repo = data["repo"]
    Developer_Notes = data["developer_notes"]



    new_id = diary_entry(Developer, Project, Start_Time, End_Time, Repo, Developer_Notes)
    return jsonify({"message": "Diary entry added", "entry_id": new_id}), 201


#information to be printed after a specific id is looked up
@app.route("/diary/<int:entry_id>", methods=["GET"])
def get_entry(entry_id):
    result = sCHOICEID(entry_id)
    if result:
        developer, project, start_time, end_time, time_worked, diary_entry, repo, dev_notes = result
        return jsonify({
            "developer": developer,
            "project": project,
            "start_time": start_time,
            "end_time": end_time,
            "time_worked": time_worked,
            "diary_entry": diary_entry,
            "repository": repo,
            "developer_notes": dev_notes
        }), 200
    else:
        return jsonify({"error": "Invalid entry ID"}), 404


#Information to be printed when searching for a specific developer name
@app.route("/diary/developer/<string:developer_name>", methods=["GET"])
def get_entries_by_developer(developer_name):
    if 'username' not in session:
        return jsonify({"error": "You must be signed in to search entries."}), 403
    
    results = sdevname(developer_name)
    if results:
        return jsonify(results), 200
    else:
        return jsonify({"error": "No entries found for this developer"}), 404
    
#Information to be printed when searching for a specific project name
@app.route("/diary/project/<string:project_name>", methods=["GET"])
def get_entries_by_project(project_name):
    if 'username' not in session:
        return jsonify({"error": "You must be signed in to search entries."}), 403
    
    results = sprojname(project_name)
    if results:
        return jsonify(results), 200
    else:
        return jsonify({"error": "No entries found for this project"}), 404

#prints all entries found
@app.route("/diary/all", methods=["GET"])
def get_all_entries():
    results = allentries()
    return jsonify(results), 200


#gives user their entries they are able to delete, asks which specific one to delete and then deletes it
@app.route("/diary/delete/<int:entry_id>", methods=["DELETE"])
def delete_diary_entry(entry_id):
    user = request.args.get("username")  # Get username from request
    if not user:
        return jsonify({"error": "Username required"}), 400

    if delete_entry(entry_id, user):
        return jsonify({"message": "Entry deleted successfully"}), 200
    else:
        return jsonify({"error": "Entry not found or unauthorized"}), 403

