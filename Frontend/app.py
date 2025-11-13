from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from scripts.klassenlisten_digitalisierung.src.app.get_classes import run as get_classes
from scripts.klassenlisten_digitalisierung.src.app.user_handler import verify_user
from scripts.klassenlisten_digitalisierung.src.app.get_lessons import run as get_lessons

import json
import os
import subprocess
import logging
import hashlib

app = Flask(__name__)
CORS(app)

@app.route('/')

def home():
    print("Aktuelles Verzeichnis:", os.getcwd())
    return render_template('index.html')

@app.route('/table_teacher')
def table_teacher():
    json_data = get_lessons("02TSBR", "1.Hj")
    class_data = json.loads(json_data)
    class_name = class_data[0]['class_name']
    lessons = class_data[0]['lessons']
    return render_template('table_teacher.html', lesson_data=lessons, class_name=class_name)

#Methode gibt eine liste der angefragten klassen zurück
@app.route("/api/classes",methods=["GET"])
def get_school_classes():
    filter = request.args.get("school_classes")
    if not filter:
       return jsonify("Error: Missing argument in get_school_classes")
    data = get_classes(filter)
    data = json.loads(data)
    return jsonify(data)

#Methode gibt simple,advanced zurück wenn benutzer valide ist. Ansonsten fehler
@app.route("/api/verify_user",methods=["GET"])
def get_authentification():
    user = request.args.get("user")
    if not user:
       return jsonify("Error: Missing argument in authentification Code:Username")

    password = request.args.get("password")
    if not password:
       return jsonify("Error: Missing argument in authentification Code:Password")

    auth = verify_user(user, password)
    print(f"auth:{auth}")

    return jsonify(auth)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

