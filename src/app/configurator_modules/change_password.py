# -*- coding: cp1252 -*-

import json
import os
import hashlib
import sys

current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
sys.path.append(project_root)

from src.app.user_handler import load_users_into_memory

def create_path(path, file_name) -> str:
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    file = os.path.join(project_root, path, file_name)
    return file

def reset_password():
    user_path = create_path("data", "users.json")

       # Load users
    with open(user_path, "r") as f:
        data = json.load(f)

    users = data.get("users", [])

    for user in users:
        user["password"] == "7484c5f89d12d0f7fdb8b03ce72b4694d58f9da473d2009d57f67bf43f265857"

    # Save changes back to JSON
    with open(user_path, "w") as f:
        json.dump(data, f, indent=4)

    load_users_into_memory()

def change_password():
    # Check if file exists
    user_path = create_path("data", "users.json")
    if not os.path.exists(user_path):
        print("Benutzerdatei nicht gefunden:/" + user_path)
        return

    # Load users
    with open(user_path, "r") as f:
        data = json.load(f)

    users = data.get("users", [])
    if not users:
        print("Benutzer konnten nicht geladen werden.")
        return

    # List available usernames
    print("Benutzer:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user['username']}")

    user_found = False

    while(user_found == False):
        choice = input("Waehlen Sie einen Benutzer: ").strip()

        for i in range(len(users)):
            if str(i + 1) == choice or choice == users[i]["username"]:
                selected_user_name = users[i]
                new_password = input(f"Neues Passwort fuer {selected_user_name["username"]}: ").strip()
                new_password = "sal" + new_password + "peper" 
                new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
                selected_user_name["password"] = new_password
                user_found = True
                break  
        if not user_found:
            print("Benutzer konnte nicht gefunden werden.")

    # Save changes back to JSON
    with open(user_path, "w") as f:
        json.dump(data, f, indent=4)

    load_users_into_memory()
    print(f"Passwort fuer {choice} wurde gaendert.")


# Example usage
