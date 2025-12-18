# -*- coding: utf-8 -*-
import json
import openpyxl
from .get_headers import run as get_headers
from .file_handler import initiate_file, get_next_empty_row, get_next_row_with_value
from .config.config_handler import load_config_data

# variables
classes_column_name = load_config_data("classes_column_name")
weekly_hrs_column_name = load_config_data("weekly_hrs_column_name")
half_year_column_name = load_config_data("half_year_column_name")#.encode("latin-1").decode("utf-8")

def _find_class_title_row(sheet, class_filter):
    end_row = sheet.max_row
    for row in range(1, end_row):
        cell = sheet.cell(row=row, column=sheet.min_column)
        if cell.value == class_filter:
            return row
    raise Exception("Class not found")
        
def get_lessons_from_sheet(sheet, headers, class_title):
    title_row = _find_class_title_row(sheet, class_title)
    start_row = get_next_row_with_value(sheet, title_row + 1) + 1
    end_row = get_next_empty_row(sheet, start_row)
    
    start_col = sheet.min_column
    end_col = sheet.max_column
    lesson_list = []
    
    for row in range(start_row, end_row):
        lesson = {}
        for col in range(start_col, end_col):
            cell = sheet.cell(row, col)
            if headers[col-1] == f"{weekly_hrs_column_name}_SuS":
                try:
                    lesson[headers[col-1]] = int(cell.value)
                except(TypeError):
                    lesson[headers[col-1]] = 0
            elif headers[col-1] == f"{weekly_hrs_column_name}_KuK":
                try:
                    lesson[headers[col-1]] = float(cell.value)
                except(TypeError):
                    lesson[headers[col-1]] = 0
            else:
                lesson[headers[col-1]] = f"{cell.value}"
        if lesson[f"{weekly_hrs_column_name}_SuS"] == "None":
            lesson[f"{weekly_hrs_column_name}_SuS"] = 0
        if lesson[f"{weekly_hrs_column_name}_KuK"] == "None":
            lesson[f"{weekly_hrs_column_name}_KuK"] = 0
        lesson_list.append(lesson)
    return lesson_list
    
def process_lessons(class_title, contrary_year_half, lessons):
    list = []
    sum_sus = 0
    sum_kuk = 0
    
    try:
        for i in range(0, len(lessons)):
            lesson = lessons[i]
            try:
                if contrary_year_half not in lesson[half_year_column_name]:
                    if "," in lesson[classes_column_name]:
                        classes = str.split(lesson[classes_column_name], ",")
                        comment = "gekoppelt mit"
                        for class_name in classes:
                            if class_name != class_title:
                                comment += f" {class_name},"
                        lesson['comment'] = comment[:len(comment) - 1]

                        while lesson['Fach'] == lessons[i + 1]['Fach'] and lesson[half_year_column_name] == lessons[i+1][half_year_column_name]:
                            if lessons[i+1][f"{weekly_hrs_column_name}_SuS"] != "None":
                                lesson[f"{weekly_hrs_column_name}_SuS"] += int(lessons[i+1][f"{weekly_hrs_column_name}_SuS"])
                            if lessons[i+1][f"{weekly_hrs_column_name}_KuK"] != "None":
                                lesson[f"{weekly_hrs_column_name}_KuK"] += float(lessons[i+1][f"{weekly_hrs_column_name}_KuK"])
                            lessons.pop(i+1)
            except(IndexError): 
                pass      
            sum_sus += int(lesson[f"{weekly_hrs_column_name}_SuS"])
            sum_kuk += float(lesson[f"{weekly_hrs_column_name}_KuK"])
                    
            list.append(lesson)
    except(IndexError):
        pass # basically ignore and continue
    
    sum_sus = round(sum_sus*100)/100
    sum_kuk = round(sum_kuk*100)/100 
    
    return {"class_name": f"{class_title}", "lessons": list, "Sum_SuS": sum_sus, "Sum_KuK": sum_kuk}

def run(class_title, year_half):
    contrary_year_half = year_half
    if "1" in year_half:
        contrary_year_half= str.replace(contrary_year_half, "1", "2")
    elif "2" in year_half:
        contrary_year_half= str.replace(contrary_year_half, "2", "1")
    
    workbook = initiate_file()
    sheet = workbook.active
    
    headers = json.loads(get_headers())
    lessons = get_lessons_from_sheet(sheet, headers, class_title)
    lesson_list = process_lessons(class_title, contrary_year_half, lessons)
    lesson_json = json.dumps(lesson_list)
    return lesson_json

result = run("02TSFR", "1.Hj")
print(result)
