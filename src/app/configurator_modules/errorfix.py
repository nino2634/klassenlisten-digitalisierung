# -*- coding: cp1252 -*-
import json
import os

#Deafult User values
DEFAULT_USERS = {
    "users": [
        {
            "username": "LUSD",
            "password": "7484c5f89d12d0f7fdb8b03ce72b4694d58f9da473d2009d57f67bf43f265857",
            "mode": "advanced"
        },
        {
            "username": "Lehrer",
            "password": "7484c5f89d12d0f7fdb8b03ce72b4694d58f9da473d2009d57f67bf43f265857",
            "mode": "simple"
        }
    ]
}

# Default config values
DEFAULT_CONFIG = {
    "excel_file": "src/app/data/Datenquelle.xlsx",
    "row_diff_class_name_headers": "3",
    "row_diff_weekly_hrs": "1",
    "half_year_column_name": "Periodizität",
    "weekly_hrs_column_name": "WoStd",
    "subject_column_name": "Fach",
    "teacher_column_name": "Lehrer",
    "classes_column_name": "Klasse(n)",
    "odd_week_value": "u-Wo",
    "even_week_value": "g-Wo"
}

def create_path(path, file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))  # script directory
    parent_dir = os.path.dirname(current_dir)                # one folder above
    return os.path.join(parent_dir, path, file_name)

def reset_config():
    config_path = create_path("config", "settings.txt")
    with open(config_path, "w", encoding="utf-8") as f:
        for key, value in DEFAULT_CONFIG.items():
            f.write(f"{key}={value}\n")
    print(f"settings.txt created at {config_path}")

def fix_config():
    config_path = create_path("config", "settings.txt")
    if not os.path.exists(config_path):
        print("Status: Fehler -> settings.txt wurde nicht gefunden")
        reset_config()
        return
    
    # Read current config
    with open(config_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    current_keys = set()
    for line in lines:
        if "=" in line:
            key = line.strip().split("=")[0]
            current_keys.add(key)
    
    missing_keys = [k for k in DEFAULT_CONFIG if k not in current_keys]
    
    if not missing_keys:
        print("Status: Kein Fehler gefunden -> settings.txt")
    else:
        print("Status: Fehler -> fehlende Schl�ssel:", ", ".join(missing_keys))
        # Append missing keys with defaults
        with open(config_path, "a", encoding="utf-8") as f:
            for key in missing_keys:
                f.write(f"{key}={DEFAULT_CONFIG[key]}\n")
        print("Fehlende Schl�ssel wurden mit Standardwerten hinzugef�gt")

def reset_users():
    users_path = create_path("data", "users.json")  # or use create_path if you want a folder
    with open(users_path, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_USERS, f, indent=4, ensure_ascii=False)
    print(f"{users_path} created with default users")
    print(f"Bitte setzen sie neue Passwoerter!")

def fix_users():
    user_path = create_path("data", "users.json")
    if not os.path.exists(user_path):
        print("Status: Fehler -> users.json wurde nicht gefunden")
        reset_users()
        return
    print("Status: Kein Fehler gefunden -> users.txt")

def fix():
    print("------------- \n Suche nach Fehler... \n -------------")
   
    fix_config()
    fix_users()

def hard_reset():
    reset_config()
    reset_users()