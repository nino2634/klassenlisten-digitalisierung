from openpyxl import Workbook
import json
from .get_lessons import run as get_lessons 

def export_file(table, class_name):
    output_file = f"/tmp/{class_name}_klassenliste.xlsx"  # absoluter Pfad

    wb = Workbook()
    ws = wb.active

    # Header aus Keys
    ws.append(list(table[0].keys()))

    # Rows
    for row in table:
        ws.append(list(row.values()))

    wb.save(output_file)
    return output_file

#export_file(json.loads(get_lessons("02TSFR", "1.Hj"))[0]['lessons'], "02TSFR")