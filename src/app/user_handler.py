from itertools import count
import json
import os
import sys 
import hashlib

from .config_handler import create_path
#from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from flask_login import UserMixin,login_user, LoginManager

users_by_id = {}

class User(UserMixin):
    def __init__(self, username, password, mode):
        self.id = username
        self.username = username
        self.password = password
        self.mode = mode

# ---------------------------
# User-Verification
# ---------------------------
def verify_user(user_i, password_i):
    user : User = users_by_id.get(user_i)

    if user is None:
        print("no user found")
        return ("Authentication Failed")

    password = "#big" + password_i + "pp"
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    target_user = ""

    if user.username == user_i: 
        print("No user found: ", user_i)
        return ("Authentication Failed")
 
    if user.password == hashed_password:
        login_user(user)
        print("user:", user.username, " has a session in flask login")
        return user.mode
    else:
        print("user is invalid: password wrong")
        return "Authentication failed"
    

def setup_user_loader(login_manager):
    load_users_into_memory()
    @login_manager.user_loader
    def load_user(user_id):
        return users_by_id.get(user_id)

def _load_user_json():
    user_path = create_path("app/data", "users.json")
    
    if not os.path.exists(user_path):
        print("Error: users.json not found.")
        return "Error: users.json not found."
    try:
        with open(user_path, "r") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        print("Error: Failed to parse users.json.")
        return "Error: Failed to parse users.json."

def load_users_into_memory():
    users_by_id.clear()
    data = _load_user_json()

    for user_server in data["users"]:
        user = User(user_server["username"],user_server["password"],user_server["mode"])
        users_by_id[user.id] = user
    
    if len(users_by_id) == 0:
        print("No user data found, check json file")