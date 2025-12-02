# -*- coding: utf-8 -*-

import json
from .file_handler import initiate_file
from .config.config_handler import load_config_data

# reads all consecutive not-empty cells in a row
# returns: column names as list
def _read_columns_in_row(sheet, row) -> list:
    values = []
    weekly_hrs_header = load_config_data("weekly_hrs_column_name")
    for column in range(sheet.min_column, sheet.max_column):
        cell = sheet.cell(row=row, column=column)
        upperCell = ""
        if(cell.value is not None):
            if cell.value == weekly_hrs_header:
                upperCell = "_"+sheet.cell(row=row-int(load_config_data("row_diff_weekly_hrs")), column=column).value # add _SuS or _KuK to WoStd
            values.append(cell.value+upperCell)
        else:
            break
    return values

def get_html_headers():
    return {
        "Fach": load_config_data("subject_column_name"),
        "WoStd_SuS": f'{load_config_data("weekly_hrs_column_name")}_SuS',
        "Lehrer": load_config_data("teacher_column_name"),
        "WoStd_KuK": f'{load_config_data("weekly_hrs_column_name")}_KuK'
    }

# reads all headers from excel file
# returns: header names as list
def _get_headers(sheet, title_row):
    headers = _read_columns_in_row(sheet=sheet, row=title_row + int(load_config_data("row_diff_class_name_headers")))
    html_headers = get_html_headers()
        
    list = []
    for header in headers:
        if header in html_headers:
            header = html_headers[header]
        #print(header)
        list.append(header)
    return list

# gets first row with value out of the excel file
# returns: list
def _read_excel_file(sheet, start_row): 
    row_count = sheet.max_row
    for row in range(start_row, row_count):
        cell = sheet.cell(row=row, column=sheet.min_column)
        if cell.value is not None:
            headers = _get_headers(sheet=sheet, title_row=row)
            return headers

# executes functions
# returns: header names as list
def run():
    workbook = initiate_file()
    sheet = workbook.active
    headers = _read_excel_file(sheet, start_row=1)
    headers_json = json.dumps(headers)
    #print(headers)
    return headers_json

result = run()
print(result)