import os

#puts together the absolute path of the a file file
#can be used in other .py to make absolut paths for files
def create_path(path, file_name) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, path, file_name)

#-----------------------------------------------------------
#Returns the matching value from the config
#-----------------------------------------------------------
def load_config_data(value_name : str) -> str:
    settings_path = create_path("", "settings.txt")

    if not os.path.exists(settings_path):
        print("Error: settings.txt not found.")
        return
    else:
        with open(settings_path) as f:
            lines = f.readlines()
    #print(lines)
    value = ""

    for line in lines:
        #print(line)
        if line.startswith(value_name + "="):
            value = line.split('=', 1)[1].strip()
            break

    if value == "":
        print("Error: No value matching key: " + value_name)
        return

    return value
