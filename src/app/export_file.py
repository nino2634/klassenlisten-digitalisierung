from openpyxl import Workbook

def run(table, output_file="export.xlsx"):
    wb = Workbook()
    ws = wb.active

    # Header aus Keys
    ws.append(list(table[0].keys()))

    # Rows
    for row in table:
        ws.append(list(row.values()))

    wb.save(output_file)
    return output_file
