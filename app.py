# -*- coding: utf-8 -*-
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_file,redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager,logout_user,login_required,current_user

import pandas as pd
from io import BytesIO

from src.app import progress_handler
from src.app.user_handler import setup_user_loader,verify_user, load_users_into_memory
from src.app.get_classes import run as get_classes
from src.app.get_lessons import run as get_lessons
from src.app.get_headers import run as get_headers
from src.app.progress_handler import save,load_all

import json
import os
import subprocess
import logging
import hashlib

app = Flask(__name__, static_url_path="/static", static_folder="static")
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# secret key for authentication
app.secret_key = "supergeheim-und-einzigartig"  
classes = get_classes("")


#For Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"
setup_user_loader(login_manager)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('filter_teacher'))
    else:
        return render_template('index.html')

@app.route('/classView')
@login_required
def filter_teacher():
    return render_template('classView.html')

@app.route('/api/classViewDetailed', methods=["GET"])
@login_required
def get_class_view_detailed_data():
    """
    Liefert die detaillierten Daten für eine bestimmte Klasse zurück.
    Parameter: "class_name": string
               "half_year": string
    Gibt zurück: JSON-Objekt mit den Details der Klasse
    """
    class_name_url_param = request.args.get("class_name")
    half_year = request.args.get("half_year")
    
    #Python Funktion aufrufen, um Daten aus Excel Liste auszulesen
    json_data = get_lessons(class_name_url_param, half_year)
    headers = json.loads(get_headers())
    class_data = json.loads(json_data or "[]")

    if not class_data:
        return "No data found for class: " + class_name_url_param, 404
    
    class_name = class_data['class_name']
    lessons = class_data['lessons']
    Sum_SuS = class_data['Sum_SuS']
    Sum_KuK = class_data['Sum_KuK']

    return jsonify({
        "class_name": class_name,
        "headers": headers,
        "lessons": lessons,
        "Sum_SuS": Sum_SuS,
        "Sum_KuK": Sum_KuK
    })

@app.route("/classViewDetailed")
@login_required
def class_view_detailed():
    return render_template("classViewDetailed.html")

#Methode gibt eine Liste der angefragten Klassen zurück
@app.route("/api/classes",methods=["GET"])
@login_required  
def get_school_classes():
    """
    führt einen Filter auf die Klassenliste aus und gibt die gefilterte Liste zurück.
    Erwartet: String oder nichts als Query-Parameter "school_classes"
    Gibt zurück: JSON-Array der gefilterten Klassenliste
    """
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
    #progress_handler.check_and_reset()
    data = request.get_json()
    term = data.get("savedHalfYear")
    print(term)

    if not term:
       return jsonify("Error: Missing argument in authentification Code: savedHalfYear")

    try:
        return jsonify(load_all(term))
    except:
        return jsonify("Error: something unexpected happend while loading progress")


#Methode gibt simple,advanced zurück wenn benutzer valide ist. Ansonsten fehler
@app.route("/api/save_progress", methods=["POST"])
def save_progress():
    data = request.get_json()
    school_class = data.get("className")
    half_year = data.get("savedHalfYear")
    state = str(data.get("checkboxState"))
    print(school_class)
    print(half_year)
    print(state)
    if not school_class:
        return jsonify({"error": "Missing argument: className"}), 400
    if not state:
        return jsonify({"error": "Missing argument: checkboxState"}), 400
    if not half_year:
        return jsonify({"error": "Missing argument: savedHalfYear"}), 400

    try:
        save(school_class, state, half_year)
        return jsonify({"success": "Saved data successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Something went wrong when saving"}), 500

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
        return jsonify({"state": "teacher"})
    if mode == "advanced":
        return jsonify({"state": "lusd"})
    else:
        return jsonify({"status": "failed", "message": "Ungültige Zugangsdaten"}), 401

@app.route("/logout")
@login_required  # optional, nur für eingeloggte Benutzer
def logout():
    logout_user()
    return jsonify("logged out")


@app.route("/api/export", methods=["POST"])
def export():
    """
    Nimmt eine JSON-Tabelle entgegen und exportiert diese als Excel-Datei.
    Erwartet: JSON-Array von Objekten, wobei jedes Objekt eine Zeile in der Tabelle darstellt.
    Gibt zurück: Excel-Datei
    """
    table = request.get_json()
    print(table)

    #Pandas Dataframe aus der Tabelle erstellen
    df_1 = pd.DataFrame(table)

    #Output Stream erstellen
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    #Workbook und Worksheet erstellen
    df_1.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1", index=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    format = workbook.add_format()
    format.set_bg_color('#eeeeee')

    #Writer wieder schließen
    writer.close()

    #Stream zurücksetzen
    output.seek(0)

    #Datei als "export.xlsx" zurückgeben
    return send_file(output, download_name="export.xlsx", as_attachment=True)

if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=8443,ssl_context=("src/app/certificate/cert.pem", "src/app/certificate/key.pem")
#     )
    app.run(host='0.0.0.0', debug=True, port=8443)
