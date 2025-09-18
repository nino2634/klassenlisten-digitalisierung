import os

def load_data_file_path() -> str:
    data_path = create_data_path()
    with open(data_path) as f:
        lines = f.readlines()
    print(lines)

def _create_data_path() -> str:
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    config_file = os.path.join(project_root, "config", "settings.txt")

    print(config_file)
    return config_file

load_data_file_path()
