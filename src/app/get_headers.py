import openpyxl
from config_handler import Config_Handler
## ToDo
## please add "_" to private classes
## add descriptions for the other methods

# gets file path from config_handler
# returns: String
def _initiate_file():
    data_file = Config_Handler()
    file_path = data_file.load_data_file_path()
    return file_path

#reads all consecutive not-empty cells in a row
def _read_columns_in_row(sheet, row) -> list:
    values = []
    for column in range(1, 100):
        cell = sheet.cell(row=row, column=column)
        if(cell.value is not None):
            values.append(cell.value)
        else:
            break
    return values

# reads all headers from excel file
# returns: list 
def _get_headers(sheet, title_row):
    headers = _read_columns_in_row(sheet=sheet, row=title_row + 3) # wir schauen hier nochmal in den großen Listen, was der Abstand ist, 3 Zielen im Testding
    list = []
    for header in headers:
        #print(header)
        list.append(header)
    return list

# gets first row with value out of the excel file
# returns: list
def _read_excel_file(sheet, start_row): 
    row_count = sheet.max_row
    for row in range(start_row, row_count):
        cell = sheet.cell(row=row, column=1)
        if cell.value is not None:
            headers = _get_headers(sheet=sheet, title_row=row)
            return headers

# executes functions
# returns: list
def run():
    file_path = _initiate_file()
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = _read_excel_file(sheet, start_row=1)
    for header in headers:
        print(header)
    return headers
