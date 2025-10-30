import json
import os

def _create_users_path(self) -> str:
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    users_file = os.path.join(project_root, "app/data", "users.json")

    return users_file

settings_path = _create_users_path()
with open(settings_path) as f:
    lines = f.readlines()
        
for line in lines:
    if line.startswith("EXCEL_FILE="):
        excel_path = line.split('=', 1)[1].strip()
    break
