import openpyxl

file_path = "/home/niklas/Coding/klassenlisten-digitalisierung/src/app/data/Datenquelle.xlsx"

def read_openpyxl():
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    row_count = sheet.max_row

    for row in range(row_count):
        if row > 0:
            cell=sheet.cell(row=row, column=1)

            print(cell.value)

read_openpyxl()