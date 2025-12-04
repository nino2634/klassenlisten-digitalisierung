import json
import os

#loads the of the current progress
current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, "data", "progress.json")

#Called on Initilistion of class
def setup():
    os.makedirs(os.path.dirname(path), exist_ok=True)

    #Create file if not found in path
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"class": []}, f, indent=4)
        return

    #Attempts to open the json to check the sturcture for errors
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict) or "class" not in data or not isinstance(data["class"], list):
            raise ValueError("Invalid structure")

    #error for handling corrupted json
    except Exception:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"class": []}, f, indent=4)

#Method to change state of a class, states are stored as a string, true = done, false = not done
def save(target_school_class: str, state: str, term: str):
    with open(path, "r") as f:
        data = json.load(f)

    #ensure the key exists in json
    if "class" not in data:
        data["class"] = []

    school_classes = data["class"]

    #structure for new entry
    new_entry = {
        "class": target_school_class,
        "state": state,
        "term": term
    }

    updated = False

    #changes entry if one exsists
    for school_class_json in school_classes:
        if (school_class_json["class"] == target_school_class and
            school_class_json["term"] == term):
            school_class_json["state"] = state
            updated = True
            break

    #adds new entry if not
    if not updated:
        school_classes.append(new_entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

#returns all class entrys inside the json
def load_all(term: str):
    with open(path, "r") as f:
        data = json.load(f)

    school_classes = data.get("class", [])
    result = [entry for entry in school_classes if entry.get("term") == term]
    return result

#resets all progress
def reset():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"class": []}, f, indent=4)

#do setup on initialization
setup()