import json
import openpyxl
from .get_headers import run as get_headers
from .file_handler import initiate_file, get_next_empty_row, get_next_row_with_value
from .config.config_handler import load_config_data

# variables
half_year_column_name = load_config_data("half_year_column_name")
classes_column_name = load_config_data("classes_column_name")
weekly_hrs_column_name = load_config_data("weekly_hrs_column_name")
odd_week_value = load_config_data("odd_week_value")
even_week_value= load_config_data("even_week_value")

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
    
def check_split_of_class(lesson1, lesson2):
    return True
    
def generate_comments(lesson):
    comments={
        "split":"Die Klasse wird aufgeteilt.\n",
        "merge":"Die Klassen werden zusammengeführt.\n",
        "odd_week":"Die Stunde findet in der ungeraden Woche statt.\n",
        "even_week":"Die Stunde findet in der geraden Woche statt.\n"
    }
    
    comment = ""
    
    if even_week_value in lesson[half_year_column_name]:
        comment += comments["even_week"]
    if odd_week_value in lesson[half_year_column_name]:
        comment += comments["odd_week"]
    if "," in lesson[classes_column_name]:
        comment += comments["merge"]
        
    return comment
    #elif check_split_of_class(lesson, nextLesson):
    #    return comments["split"]
    
    # elif: multiple lessons of same LV-Id with different classes = split
    
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
        if year_half in lesson[load_config_data("half_year_column_name")]:
            lesson['comment'] = generate_comments(lesson)
            list.append(lesson)
    
    sum_sus = 0
    sum_kuk = 0
    
    for lesson in list:
        #print(lesson['comment'])
        if lesson[f"{weekly_hrs_column_name}_SuS"] !='None':
            sum_sus += int(lesson[f"{weekly_hrs_column_name}_SuS"])
        if lesson[f"{weekly_hrs_column_name}_KuK"] != 'None':
            sum_kuk += float(lesson[f"{weekly_hrs_column_name}_KuK"])
    
    lesson_list.append({"class_name": f"{class_title}", "lessons": list, "Sum_SuS": sum_sus, "Sum_KuK": sum_kuk})
    return lesson_list

def run(class_title, year_half):
    workbook = initiate_file()
    sheet = workbook.active
    headers = json.loads(get_headers())
    lesson_list = _get_lessons_by_class(sheet, class_title, year_half, headers)  
    lesson_json = json.dumps(lesson_list)  
    #print(lesson_list[0]['lessons'])
    return lesson_json

run("02TSFR", "1.Hj")