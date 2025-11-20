# -*- coding: cp1252 -*-

import os


def create_path(folder, file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    return os.path.join(parent_dir, folder, file_name)


def show_config():
    """Print all key=value pairs in settings.txt"""
    config_path = create_path("config", "settings.txt")
    if not os.path.exists(config_path):
        print("settings.txt does not exist.")
        return

    print("\nEinstellungen:")
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                print(f"  {line}")
    print()  # extra line for spacing

def update_config(key: str, new_value: str):
    """Update a key=value pair in settings.txt. Stops if key does not exist."""
    config_path = create_path("config", "settings.txt")

    if not os.path.exists(config_path):
        print("Fehler: settings.txt fehlt. Benutzen Sie die Fehlersuche.")
        return

    # Read current settings
    with open(config_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    key_found = False
    for i, line in enumerate(lines):
        line_strip = line.strip()
        if not line_strip or "=" not in line_strip:
            continue
        current_key, _ = line_strip.split("=", 1)
        if current_key == key:
            lines[i] = f"{key}={new_value}\n"
            key_found = True
            break

    if not key_found:
        print(f"Fehler: Einstellung '{key}' ist nicht vorhanden.")
        return

    # Write back the updated config
    with open(config_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Einstellungen geaendert: {key}={new_value}")

def change_settings():
    show_config()
    choice = input("Welche Einstellung?")
    new_value = input("Geben Sie einen neuen Wert an.")
    update_config(choice,new_value)