import csv
import openpyxl

file_path = "/home/niklas/Coding/klassenlisten-digitalisierung/src/app/data/Datenquelle.xlsx"

def read_csv():
    with open(file=file_path, newline="") as csvfile:
        print(csvfile)

def read_openpyxl():
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    cell=sheet.cell(2, 1)

    print(cell.value)

read_openpyxl()