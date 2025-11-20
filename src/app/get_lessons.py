import json
import openpyxl
from .get_headers import run as get_headers
from .file_handler import initiate_file, get_next_empty_row, get_next_row_with_value
from .config.config_handler import load_config_data

def _find_class_title_row(sheet, class_filter):
    end_row = sheet.max_row
    for row in range(1, end_row):
        cell = sheet.cell(row=row, column=sheet.min_column)
        if cell.value == class_filter:
            return row
    raise Exception("Class not found")

def _get_lessons_by_class(sheet, class_title, year_half, headers):
    title_row = _find_class_title_row(sheet, class_title)
    start_row = get_next_row_with_value(sheet, title_row + 1) + 1
    end_row = get_next_empty_row(sheet, start_row)

    start_col = sheet.min_column
    end_col = sheet.max_column
    lesson_list = []
    list = []
    for row in range(start_row, end_row):
        lesson = {}
        for col in range(start_col, end_col):
            cell = sheet.cell(row, col)
            header = headers[col-1]
            lesson[header] = f"{cell.value}"
        if year_half in lesson[load_config_data("half_year_name_column")]:
            list.append(lesson)
    lesson_list.append({"class_name": f"{class_title}", "lessons": list})
    return lesson_list

def run(class_title, year_half):
    workbook = initiate_file()
    sheet = workbook.active
    headers = json.loads(get_headers())
    lesson_list = _get_lessons_by_class(sheet, class_title, year_half, headers)  
    lesson_json = json.dumps(lesson_list)  
    #print(lesson_list[0]['lessons'])
    return lesson_json

run("02TSBR", "1.Hj")