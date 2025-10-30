import json
import os
import sys
from .config_handler import create_path

#validates users, returns simple or advanced if user is valid, 
#otherwise returns error string

def run(user,hash):
    #open file path and verify data integrity
    settings_path = create_path("app/data", "users.json")
    
    if not os.path.exists(settings_path):
        print("Error: users.json not found.")
        return
    try:
        with open(settings_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: Failed to parse users.json.")
        return

    #actual user verification
    for user_server in data["users"]:
        if user_server["username"] == user: 
            target_user = user_server

    if target_user["username"] == "":
        print("user is invalid: no user found" + target_user)
        return

    if target_user["password"] == hash:
        print(target_user["mode"])
        return
    else:
        print("user is invalid: password wrong")
        return


#only for testing
run("Fabian","passwort123hashed")

