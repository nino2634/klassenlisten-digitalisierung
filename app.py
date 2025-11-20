from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from flask_login import LoginManager,logout_user,login_required

from src.app.user_handler import setup_user_loader
from src.app.get_classes import run as get_classes
from src.app.user_handler import verify_user, load_users_into_memory
from src.app.get_lessons import run as get_lessons
from src.app.export_file import export_file

import json
import os
import subprocess
import logging
import hashlib

app = Flask(__name__)
CORS(app)

# secret key for authentication
app.secret_key = "supergeheim-und-einzigartig"  

#For Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
setup_user_loader(login_manager)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/teacherView')
@login_required
def filter_teacher():
    return render_template('teacherView.html')

@app.route('/api/teacherDetailed', methods=["GET"])
@login_required
def table_teacher_detailed(class_name_url_param, half_year):
    class_name_url_param = request.args.get("class_name")
    half_year = request.args.get("half_year")
    json_data = get_lessons(class_name_url_param, half_year)
    class_data = json.loads(json_data)
    class_name = class_data[0]['class_name']
    lessons = class_data[0]['lessons']
    return render_template('teacherView.html')

#Methode gibt eine Liste der angefragten Klassen zurück
@app.route("/api/classes",methods=["GET"])
@login_required  
def get_school_classes():
    filter = request.args.get("school_classes")
        # Wenn kein Filter angegeben ist → alle Klassen liefern
    if not filter:
        data = get_classes("")  # oder get_classes(None)
    else:
        data = get_classes(filter)

    data = json.loads(data)
    return jsonify(data)

#Methode gibt simple,advanced zurück wenn benutzer valide ist. Ansonsten fehler
@app.route("/api/verify_user",methods=["POST"])
def get_authentification():
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
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route("/export", methods=["POST"])
@login_required
def export():
    table_data = request.get_json()
    excel_file = export_file(table=table_data)
    return jsonify({"Status": "OK", "file":excel_file})

@app.route("/download")
@login_required
def download():
    file_path = os.path.join(os.getcwd(), "export.xlsx")  # absoluter Pfad
    if not os.path.exists(file_path):
        return "Datei existiert nicht!", 404
    return send_file(file_path, as_attachment=True)
