import json
import os
from turtle import update

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, "data", "progress.json")

def setup():
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            data = {}
            json.dump(data, f, indent=4, ensure_ascii=False)
   
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, "data", "progress.json")

def setup():
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"class": []}, f, indent=4, ensure_ascii=False)

def save(target_school_class: str, state: bool, term: int):
    with open(path, "r") as f:
        data = json.load(f)

    # ensure the key exists
    if "class" not in data:
        data["class"] = []

    school_classes = data["class"]

    new_entry = {
        "class": target_school_class,
        "state": state,
        "term": term
    }

    updated = False
    for school_class_json in school_classes:
        if (school_class_json["class"] == target_school_class and
            school_class_json["term"] == term):
            school_class_json["state"] = state
            updated = True
            break

    if not updated:
        school_classes.append(new_entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_all(term: int):
    with open(path, "r") as f:
        data = json.load(f)

    school_classes = data.get("class", [])
    result = [entry for entry in school_classes if entry.get("term") == term]

    return result

setup()