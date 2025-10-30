import json
import openpyxl
import config_handler

def _initiate_file():
    filePath = config_handler.load_data_file_path()
    return filePath

def run(class_filter):
    filePath = _initiate_file()
    workbook = openpyxl.load_workbook(filePath)
    sheet = workbook.active
    