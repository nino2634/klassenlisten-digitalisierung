import os

current_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(current_dir, "settings.txt")

#Returns the matching value from the config
def load_config_data(value_name : str) -> str:
    """
    Sucht in der settings.txt nach dem übergebenen Key und gibt den zugehörigen Wert zurück.
    
    :param value_name: String, Name des Keys
    
    returns: String, gefundener Wert
    """

    # sucht nach der settings.txt im aktuellen Verzeichnis
    if not os.path.exists(settings_path):
        print("Error: settings.txt not found.")
        return
    else:
        with open(settings_path) as f:
            lines = f.readlines()

    value = ""

    #liest Wert aus der settings.txt aus
    for line in lines:
        if line.startswith(value_name + "="):
            value = line.split('=', 1)[1].strip()
            break

    if value == "":
        print("Error: No value matching key: " + value_name)
        return

    return value
