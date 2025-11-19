import os
import sys
import json
import hashlib
from itertools import count

from flask_login import UserMixin, login_user, LoginManager
from .config_handler import create_path

# ---------------------------------------------------------
# Globale Benutzer-Sammlung:
# Enthält alle geladenen Benutzerobjekte, indexiert nach Benutzername.
# ---------------------------------------------------------
users_by_id = {}


# ---------------------------------------------------------
# Benutzerklasse
# ---------------------------------------------------------
class User(UserMixin):
    """
    Repräsentiert einen Benutzer des Systems.
    Erbt von Flask-Login's UserMixin, um Sitzungsmanagement zu ermöglichen.
    """
    def __init__(self, username, password, mode):
        self.id = username                 # Flask-Login erwartet eine ID-Property
        self.username = username           # Benutzername (gleichzeitig Primärschlüssel)
        self.password = password           # Gespeichertes Passwort (gehasht)
        self.mode = mode                   # Zugriffsmodus/Rolle (z.B. admin, user, etc.)


# ---------------------------------------------------------
# Lädt Benutzerdaten aus der JSON-Datei.
# ---------------------------------------------------------
def _load_user_json():
    """
    Liest die Datei 'users.json' ein und gibt die Daten als Python-Objekt zurück.
    Erwartet ein Format wie:
    {
        "users": [
            {"username": "...", "password": "...", "mode": "..."}
        ]
    }
    """
    user_path = create_path("app/data", "users.json")
    
    # Prüfen, ob Datei existiert
    if not os.path.exists(user_path):
        print("Error: users.json not found.")
        return "Error: users.json not found."
    
    # JSON-Daten einlesen
    try:
        with open(user_path, "r") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        print("Error: Failed to parse users.json.")
        return "Error: Failed to parse users.json."


# ---------------------------------------------------------
# Lädt alle Benutzer aus der JSON-Datei in den Speicher.
# ---------------------------------------------------------
def load_users_into_memory():
    """
    Lädt alle Benutzer aus der JSON-Datei in das globale Dictionary 'users_by_id'.
    Jeder Benutzer wird als User-Objekt gespeichert.
    """
    users_by_id.clear()
    data = _load_user_json()

    # Benutzer aus der JSON-Struktur in Objekte umwandeln
    for user_data in data["users"]:
        user = User(user_data["username"], user_data["password"], user_data["mode"])
        users_by_id[user.id] = user
    
    if len(users_by_id) == 0:
        print("No user data found, check json file")


# ---------------------------------------------------------
# Verifiziert einen Benutzer bei der Anmeldung.
# ---------------------------------------------------------
def verify_user(username_input, password_input):
    """
    Überprüft Benutzername und Passwort.
    Falls gültig, wird der Benutzer über Flask-Login eingeloggt.

    Rückgabewerte:
        - Benutzerrolle (mode), falls Authentifizierung erfolgreich.
        - "Authentication failed" bei Fehlern.
    """
    user: User = users_by_id.get(username_input)

    # Benutzer existiert nicht
    if user is None:
        print("no user found")
        return "Authentication Failed"

    # Passwort salzen und hashen
    password = "#big" + password_input + "pp"
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Passwortvergleich
    if user.password == hashed_password:
        login_user(user)
        print("user:", user.username, "has a session in flask login")
        return user.mode
    else:
        print("user is invalid: password wrong")
        return "Authentication failed"


# ---------------------------------------------------------
# Flask-Login User-Loader konfigurieren.
# ---------------------------------------------------------
def setup_user_loader(login_manager):
    """
    Registriert die Flask-Login-Funktion zum Laden eines Benutzers aus der Sitzung.
    Muss beim Start der App einmal aufgerufen werden.
    """
    load_users_into_memory()

    @login_manager.user_loader
    def load_user(user_id):
        # Gibt das User-Objekt anhand der gespeicherten ID (Benutzername) zurück
        return users_by_id.get(user_id)