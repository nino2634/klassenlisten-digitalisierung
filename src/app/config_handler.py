import os

#puts together the absolute path of the a file file
#can be used in other .py to make absolut paths for files
def create_path(path, file_name) -> str:
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    file = os.path.join(project_root, path, file_name)

    return file

#config method to get the config path
#will be called multiple times since path is not saved
def load_data_file_path() -> str:
    settings_path = create_path("app/config", "settings.txt")
    #WE STOPPED HERE!!!!!
    if not os.path.exists(settings_path):
        print("Error: settings.txt not found.")
        return
    else:
        with open(settings_path) as f:
            lines = f.readlines()
        
    for line in lines:
        if line.startswith("EXCEL_FILE="):
            excel_path = line.split('=', 1)[1].strip()
        break
    print(excel_path)
    return excel_path
