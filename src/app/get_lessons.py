import json
import openpyxl
from .config_handler import load_data_file_path

def _initiate_file():
    filePath = load_data_file_path()
    return filePath

def _find_class_title_row(sheet, class_filter):
    end_row = sheet.max_row
    for row in range(1, end_row):
        cell = sheet.cell(row=row, column=1)
        if cell.value == class_filter:
            return row
    raise Exception("Class not found")

def _get_next_empty_row(sheet, start_row):
    end_row = sheet.max_row
    for row in range(start_row, end_row):
        cell = sheet.cell(row=row, column=1)
        if(cell.value is None):
            return row
    return end_row + 1

def _get_lessons_by_class(sheet, class_title):
    title_row = _find_class_title_row(sheet, class_title)
    spacer:int = 3 # noch anpassen, wenn Liste von Landsiedel bekommen
    start_row = title_row + spacer
    end_row = _get_next_empty_row(sheet=sheet, start_row=start_row)

    lesson_list = []
    for row in range():
        print(x)

def run(class_title):
    filePath = _initiate_file()
    workbook = openpyxl.load_workbook(filePath)
    sheet = workbook.active
    lesson_list = _get_lessons_by_class(sheet, class_title)    


run("02TSBR")