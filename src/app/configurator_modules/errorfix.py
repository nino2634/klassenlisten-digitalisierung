# -*- coding: cp1252 -*-

import os

def create_path(path, file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))  # script directory
    parent_dir = os.path.dirname(current_dir)                # one folder above
    return os.path.join(parent_dir, path, file_name)

def reset_config():
    config_path = create_path("config", "settings.txt")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write("excel_file=src/app/data/Datenquelle.xlsx\n")
        f.write("half_year_column_name=Periodizität\n") 
        f.write("weekly_hrs_column_name=WoStd\n") 
        f.write("row_diff_weekly_hrs=1\n") 

def fix_config():
    config_path = create_path("config", "settings.txt")
    if not os.path.exists(config_path):
        print("Status: Fehler ->settings.txt wurde nicht gefunden")
        reset_config()  
        print("settings have been created with deafult settings")
        return
    print("Status:OKAY settings.txt")

def fix_users():
    user_path = create_path("data", "users.json")

def fix():
    fix_config()

def hard_reset():
    reset_config()