# -*- coding: utf-8 -*-
import json
import openpyxl
from .get_headers import run as get_headers
from .file_handler import initiate_file, get_next_empty_row, get_next_row_with_value
from .config.config_handler import load_config_data

# variables
classes_column_name = load_config_data("classes_column_name")
weekly_hrs_column_name = load_config_data("weekly_hrs_column_name")
half_year_column_name = load_config_data("half_year_column_name").encode("latin-1").decode("utf-8")

def _find_class_title_row(sheet, class_filter):
    end_row = sheet.max_row
    for row in range(1, end_row):
        cell = sheet.cell(row=row, column=sheet.min_column)
        if cell.value == class_filter:
            return row
    raise Exception("Class not found")

def add_sums(lesson_list):
    sum_sus = 0
    sum_kuk = 0
    
    for lesson in lesson_list[0]['lessons']:
        sum_sus += int(lesson['WoStd_SuS'])
        sum_kuk += int(lesson['WoStd_KuK'])
    
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
            
        if "," in lesson[classes_column_name]:
            classes = str.split(lesson[classes_column_name], ",")
            comment = "gekoppelt mit"
            for class_name in classes:
                if class_name != class_title:
                    comment += f" {class_name},"
            lesson['comment'] = comment[:len(comment) - 1]
        if year_half in lesson[half_year_column_name]:
            list.append(lesson)
    
    sum_sus = 0
    sum_kuk = 0
    
    for lesson in list:
        #print(lesson['comment'])
        if lesson[f"{weekly_hrs_column_name}_SuS"] !='None':
            sum_sus += int(lesson[f"{weekly_hrs_column_name}_SuS"])
        if lesson[f"{weekly_hrs_column_name}_KuK"] != 'None':
            sum_kuk += float(lesson[f"{weekly_hrs_column_name}_KuK"])
    
    sum_sus = round(sum_sus*100)/100
    sum_kuk = round(sum_kuk*100)/100
    
    lesson_list.append({"class_name": f"{class_title}", "lessons": list, "Sum_SuS": sum_sus, "Sum_KuK": sum_kuk})
    return lesson_list

def run(class_title, year_half):
    workbook = initiate_file()
    sheet = workbook.active
    headers = json.loads(get_headers())
    lesson_list = _get_lessons_by_class(sheet, class_title, year_half, headers)  
    lesson_json = json.dumps(lesson_list)  
    return lesson_json

#result = run("02TSFR", "1.Hj")
#print(result)
