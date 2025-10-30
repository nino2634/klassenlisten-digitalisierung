import os
from get_path import create_path

#returns the path of the excel file
def load_data_file_path() -> str:
    settings_path = create_path("app/config", "settings.txt")
    with open(settings_path) as f:
        lines = f.readlines()
        
    for line in lines:
        if line.startswith("EXCEL_FILE="):
            excel_path = line.split('=', 1)[1].strip()
        break
    print(excel_path)
    return excel_path
