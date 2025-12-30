import json
import os, hashlib

from .config.config_handler import load_config_data

current_dir = os.path.dirname(os.path.abspath(__file__))

progress_path = os.path.join(current_dir, "data", "progress.json")
save_path = os.path.join(current_dir, "data", "save.json")

#Called on initialization of class
def setup():
    """
    Stellt sicher, dass die JSON-Datei existiert und die richtige Struktur hat.
    Wirft Exception bei Fehlern, sonst kein return-Wert.
    """
    os.makedirs(os.path.dirname(progress_path), exist_ok=True)
    
    #Create file if not found in path
    if not os.path.exists(progress_path):
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump({"className": []}, f, indent=4)
        return

    #Attempts to open the json to check the structure for errors
    try:
        with open(progress_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict) or "className" not in data or not isinstance(data["className"], list):
            raise ValueError("Invalid structure")

    #error for handling corrupted json
    except Exception:
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump({"className": []}, f, indent=4)

#Method to change state of a class, states are stored as a string, true = done, false = not done
def save(target_school_class: str, state: str, term: str):
    """
    Speichert den Fortschritt einer Schulklasse in der JSON-Datei.
    Fortschritt == Eingetragen in DB oder nicht
    
    :param target_school_class: String, Name der Schulklasse
    :param state: String, "true" or "false"
    :param term: String, Halbjahr der Schulklasse
    """
    with open(progress_path, "r") as f:
        data = json.load(f)

    #ensure the key exists in json
    if "className" not in data:
        data["className"] = []

    school_classes = data["className"]

    #structure for new entry
    new_entry = {
        "className": target_school_class,
        "checkboxState": state,
        "savedHalfYear": term
    }

    updated = False

    #changes entry if one exsists
    for school_class_json in school_classes:
        if (school_class_json["className"] == target_school_class and
            school_class_json["savedHalfYear"] == term):
            school_class_json["checkboxState"] = state
            updated = True
            break

    #adds new entry if not
    if not updated:
        school_classes.append(new_entry)

    with open(progress_path, "w") as f:
        json.dump(data, f, indent=4)

#returns all class entrys inside the json
def load_all(term: str):
    with open(progress_path, "r") as f:
        data = json.load(f)

    school_classes = data.get("className", [])
    result = [entry for entry in school_classes if entry.get("savedHalfYear") == term]
    return result


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)

    return h.hexdigest()

def check_and_reset():
    data_path = load_config_data("excel_file")
    current_hash = file_hash(data_path)

    try:
        with open(save_path, "r") as f:
                data = json.load(f)
    except:
        update_save_file(current_hash)
        reset()
        return True

    #ensure the key exists in json
    #if not reset to not have duplicate values in progress (failsave)
    if "hash" not in data:
        update_save_file(current_hash)
        reset()
        return True
    else:
        saved_hash = data["hash"]

    if saved_hash == current_hash:
        return False  # no reset

    # reset progress if hash has changed
    update_save_file(current_hash)
    reset()
    return True

def update_save_file(current_hash):
    with open(save_path, "w") as f:
        new_file = {}
        new_file["hash"] = current_hash
        json.dump(new_file,f, indent=4)

#resets all progress
def reset():
    os.makedirs(os.path.dirname(progress_path), exist_ok=True)
    with open(progress_path, "w", encoding="utf-8") as f:
        json.dump({"className": []}, f, indent=4)

#do setup on initialization
check_and_reset()
setup()
