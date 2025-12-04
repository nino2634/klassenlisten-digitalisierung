import os
import sys
import json
import hashlib

from itertools import count
from flask_login import UserMixin, login_user, LoginManager

users_by_id = {}

current_dir = os.path.dirname(os.path.abspath(__file__))
user_path = os.path.join(current_dir, "data", "users.json")

#pre-made user class from flask
class User(UserMixin):
    def __init__(self, username, password, mode):
        self.id = username                
        self.username = username           
        self.password = password           
        self.mode = mode                  

#loads json of all users
def _load_user_json():
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


#Caches all users into memory
def load_users_into_memory():

    users_by_id.clear()
    data = _load_user_json()

    for user_data in data["users"]:
        user = User(user_data["username"], user_data["password"], user_data["mode"])
        users_by_id[user.id] = user
    
    if len(users_by_id) == 0:
        print("No user data found, check json file")


#verify a user, rutruns mode on sucsses
def verify_user(username_input, password_input):

    user: User = users_by_id.get(username_input)

    # user does not exsist
    if user is None:
        print("no user found")
        return "Authentication Failed"

    #salt and peper
    password = "sal" + password_input + "peper"
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    #check password
    if user.password == hashed_password:
        login_user(user)
        print("user:", user.username, "has a session in flask login")
        return user.mode
    else:
        print("user is invalid: password wrong")
        return "Authentication failed"


#registers flask login session
def setup_user_loader(login_manager):
    load_users_into_memory()

    @login_manager.user_loader
    def load_user(user_id):
        return users_by_id.get(user_id)

