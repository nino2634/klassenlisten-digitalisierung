import os

def create_path(path, file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))  # script directory
    parent_dir = os.path.dirname(current_dir)                # one folder above
    return os.path.join(parent_dir, path, file_name)

def fix_config():
    config_path = create_path("config", "settings.txt")
    if not os.path.exists(config_path):
        print("Error: settings.txt not found at: " + config_path)
    
def fix_users():
    user_path = create_path("data", "users.json")
    
def hard_reset():
    fix_config()

hard_reset()