from openpyxl import Workbook
import os

def export_file(table, output_file=None):
    if output_file is None:
        output_file = os.path.join(os.getcwd(), "export.xlsx")  # absoluter Pfad

    wb = Workbook()
    ws = wb.active

    # Header aus Keys
    ws.append(list(table[0].keys()))

    # Rows
    for row in table:
        ws.append(list(row.values()))

    wb.save(output_file)
    return output_file
