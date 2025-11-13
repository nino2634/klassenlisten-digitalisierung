from .config_handler import load_data_file_path
import openpyxl

def initiate_file():
    filePath = load_data_file_path()
    workbook = openpyxl.load_workbook(filePath)
    return workbook


def get_next_empty_row(sheet, start_row):
    end_row = sheet.max_row
    for row in range(start_row, end_row):
        cell = sheet.cell(row=row, column=sheet.min_column)
        if(cell.value is None):
            return row
        
def get_next_row_with_value(sheet, start_row):
    end_row = sheet.max_row
    for row in range(start_row, end_row):
        cell=sheet.cell(row=row, column=sheet.min_column)
        if(cell.value is not None):
            return row
