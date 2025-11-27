#import openpyxl
import json
from .file_handler import initiate_file
from .get_headers import run as get_headers

def run(class_filter=""):
    workbook = initiate_file()
    sheet = workbook.active

    classes = []
    headers = json.loads(get_headers())

    # Alle Zeilen der ersten Spalte sehr schnell durchlaufen
    for row in sheet.iter_rows(min_col=1, max_col=1, values_only=True):
        value = row[0]

        # nur Strings berücksichtigen
        if not isinstance(value, str):
            continue
        
        # filter prüfen
        if class_filter in value and value.strip() not in headers:
            classes.append(value)

    if not classes:
        return json.dumps(f"Class '{class_filter}' not found")

    return json.dumps(classes)

result = run("") 
print(result)