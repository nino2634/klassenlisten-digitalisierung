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
   

#Data manegment
def save(target_school_class: str, state: bool, term: int):
    with open(path, "r") as f:
        data = json.load(f)

    school_classes = data.get("class", [])

    new_entry = {
        "class": target_school_class,
        "state": state,
        "term": term
    }

    updated = False
    for school_class_json in school_classes:
        is_rightclass = school_class_json["class"] == target_school_class
        is_rightterm = school_class_json["term"] == term

        if is_rightclass and is_rightterm:
            school_class_json["state"] = state
            updated = True
            break

    if not updated:
        school_classes.append(new_entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_all():
	pass


setup()
save("11",False,1)