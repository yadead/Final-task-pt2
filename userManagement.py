import sqlite3
import os

database_name = "databaseFiles\database.db"
table_nameu = "user_table"
table_name = "diary_entry"
print("Database path:", os.path.abspath(database_name))

#connect sqlite3 to the database
connection = sqlite3.connect(database_name)
cursor = connection.cursor()

#Create a table if it dosent exist yet
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_nameu} (
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
""")
connection.commit()

#Create a table if it dosent exist yet
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        Entry_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Developer TEXT,
        Project TEXT,
        Start_Time TEXT,
        End_Time TEXT,
        Diary_Entry TEXT,
        Time_Worked TEXT,
        Repo TEXT,
        Developer_Notes TEXT
    );
""")
connection.commit()

#ability to input a username and password into the database
def signup(username, password):
    query = f"INSERT INTO {table_nameu} (username, password) VALUES (?, ?);"
    cursor.execute(query, (username, password))
    connection.commit()

#ability to find and return that specific username and password to check if it is valid
def signin(username, password):
    query = f"SELECT * FROM {table_nameu} WHERE username = ? AND password = ?;"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result is not None

#connect sqlite3 to the database
connection = sqlite3.connect(database_name)
cursor = connection.cursor()

#Ability to input things into the table
def diary_entry(Developer, Project, Start_Time, End_Time, Diary_Entry, Time_Worked, Repo, Developer_Notes):
    query = f"""
        INSERT INTO {table_name} (Developer, Project, Start_Time, End_Time, Diary_Entry, Time_Worked, Repo, Developer_Notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (Developer, Project, Start_Time, End_Time, Diary_Entry, Time_Worked, Repo, Developer_Notes))
    connection.commit()
    last_id = cursor.lastrowid
    return last_id

#input the id seperately into the table
def insert_id_only(entry_id):
    query = f"INSERT INTO {table_name} (Entry_ID) VALUES (?);"
    cursor.execute(query, (entry_id,))
    connection.commit()
    return

#find all entries for a specific developer name
def sdevname(sdev_name_choice): 
    query = f"SELECT Entry_ID, Developer, Project, Diary_Entry FROM {table_name} WHERE Developer = ?"
    cursor.execute(query, (sdev_name_choice,))
    dev_name_results = cursor.fetchall()
    return dev_name_results 

#find all entries for a specific project name
def sprojname(sproj_name_choice): 
    query = f"SELECT Entry_ID, Developer, Project, Diary_Entry FROM {table_name} WHERE Project = ?"
    cursor.execute(query, (sproj_name_choice,))
    proj_name_results = cursor.fetchall()
    return proj_name_results 

#grab all entries submitted
def allentries(): 
    query = f"SELECT Entry_ID, Developer, Project, Diary_Entry FROM {table_name}"
    cursor.execute(query)
    allentries_results = cursor.fetchall()
    return allentries_results 

#pick and fully view a specific entry based on its ID
def sCHOICEID(choiceid):
    query = f"SELECT Developer, Project, Start_Time, End_Time, Diary_Entry, Time_Worked, Repo, Developer_Notes FROM {table_name} WHERE Entry_ID = ?;"
    cursor.execute(query, (choiceid,))
    return cursor.fetchone()

#grabs all the entries made by the specific user
def get_user_entries(developer_name):
    query = f"SELECT Entry_ID, Developer, Project, Diary_Entry FROM {table_name} WHERE Developer = ?"
    cursor.execute(query, (developer_name,))
    return cursor.fetchall()

#deletes the entry the user has selected if it was made by the specific user
def delete_entry(entry_id, developer_name):
    cursor.execute(f"SELECT Developer FROM {table_name} WHERE Entry_ID = ?", (entry_id,))
    result = cursor.fetchone()
    if result is None:
        print("Entry not found.")
        return False
    if result[0] != developer_name:
        print("You can only delete your own entries")
        return False
    cursor.execute(f"DELETE FROM {table_name} WHERE Entry_ID = ?", (entry_id,))
    connection.commit()
    print(f"Entry {entry_id} deleted successfully")
    return True


