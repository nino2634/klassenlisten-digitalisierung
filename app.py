# -*- coding: utf-8 -*-
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from flask_login import LoginManager,logout_user,login_required

from src.app.user_handler import setup_user_loader,verify_user, load_users_into_memory
from src.app.get_classes import run as get_classes
from src.app.get_lessons import run as get_lessons
from src.app.get_headers import run as get_headers
from src.app.export_file import export_file
from src.app.progress_handler import save,load_all

import json
import os
import subprocess
import logging
import hashlib

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# secret key for authentication
app.secret_key = "supergeheim-und-einzigartig"  
classes = get_classes("")


#For Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
setup_user_loader(login_manager)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/teacherView')
#@login_required
def filter_teacher():
    return render_template('teacherView.html')

@app.route('/teacherDetailed', methods=["GET"])
@login_required
def table_teacher_detailed():
    class_name_url_param = request.args.get("class_name", "").strip()
    half_year = request.args.get("half_year", "").strip()

    json_data = get_lessons(class_name_url_param, half_year)
    headers = json.loads(get_headers())
    class_data = json.loads(json_data or "[]")

    if not class_data:
        return "No data found for class: " + class_name_url_param, 404

    class_name = class_data[0]['class_name']
    lessons = class_data[0]['lessons']
    Sum_SuS = class_data[0]['Sum_SuS']
    Sum_KuK = class_data[0]['Sum_KuK']
    return render_template('teacherDetailed.html', class_name=class_name, lessons=lessons, headers=headers, sum_SuS=Sum_SuS, sum_KuK=Sum_KuK)
#Methode gibt eine Liste der angefragten Klassen zurück
@app.route("/api/classes",methods=["GET"])
@login_required  
def get_school_classes():
    filter = request.args.get("school_classes")
    class_list = json.loads(classes) 
    
    if not filter:
        data = class_list
    if filter:
        data = []
        for c in class_list:
            if filter in c:
                data.append(c)
        
    return jsonify(data)

#Methode gibt allen Fortschrit für ein gegebenes Schuhljahr
@app.route("/api/load_progress",methods=["POST"])
@login_required  
def load_progress():
    data = request.get_json()
    term = data.get("term")

    if not term:
       return jsonify("Error: Missing argument in authentification Code:term")

    try:
        return jsonify(load_all(term))
    except:
        return jsonify("Error: something unexpected happend while loading progress")


#Methode gibt simple,advanced zurück wenn benutzer valide ist. Ansonsten fehler
@app.route("/api/save_progress",methods=["POST"])
def save_progress():
    data = request.get_json()
    school_class = data.get("class")
    term = data.get("term")
    state = data.get("state")

    if not school_class:
       return jsonify("Error: Missing argument in authentification Code:school_class")

    if not state:
       return jsonify("Error: Missing argument in authentification Code:state")

    if not term:
       return jsonify("Error: Missing argument in authentification Code:term")

    try:
        save(school_class,state,term)
        return jsonify("saved data succesfully")
    except:
        return jsonify("Error: something went wrong when saving")

#Methode gibt simple,advanced zurück wenn benutzer valide ist. Ansonsten fehler
@app.route("/api/verify_user",methods=["POST"])
def get_authentification():
    load_users_into_memory()

    data = request.get_json()
    user = data.get("user")
    password = data.get("password")

    if not user:
       return jsonify("Error: Missing argument in authentification Code:Username")

    if not password:
       return jsonify("Error: Missing argument in authentification Code:Password")

    mode = verify_user(user, password)

    if mode == "simple":
        return jsonify({"redirect_url": "/teacherView"})
    if mode == "advanced":
        return jsonify({"redirect_url": "/teacherView"})
    else:
        return jsonify({"status": "failed", "message": "Ungültige Zugangsdaten"}), 401

@app.route("/logout")
@login_required  # optional, nur für eingeloggte Benutzer
def logout():
    logout_user()
    return jsonify("logged out")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8443,ssl_context=("src/app/certificate/cert.pem", "src/app/certificate/key.pem")
    )


@app.route("/export", methods=["POST"])
def export():
    data = request.get_json()

    # Klasse aus Query oder Default
    class_name = request.args.get("class", "Unbenannt")

    file_path = export_file(data, class_name)
    print(file_path)

    return jsonify({
        "status": "ok",
        "file": file_path
    })

@app.route("/download")
def download():
    file_path = request.args.get("file")

    if not file_path:
        return "No file specified", 400

    p = Path(file_path)
    
    if not p.exists():
        return "File not found", 404

    return send_file(p, as_attachment=True)
