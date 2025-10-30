import config_handler as ch
import openpyxl

# gets file path from config_handler
# returns path of file as String
def _initiate_file():
    file_path = ch.load_data_file_path()
    return file_path

# searches all class names in excel file
# if filter is set, searches classes with specific names
# returns: class names as list
def _get_classes_from_file(sheet, start_row, class_filter): 
    classes = []
    spacer = 3 # empty rows between class name and lessons
    end_row = sheet.max_row
    row = start_row
    while end_row > row:
        cell = sheet.cell(row=row, column=1)
        if cell.value is not None:
            if(class_filter in cell.value):
                classes.append(cell.value)
            if(row+spacer < end_row):
                new_row=_skip_lessons(sheet=sheet, start_row=row+spacer, end_row=end_row)
                row = new_row
            else:
                break;
        else:
            row += 1
    return classes

# skips all lessons to get to the next class name
# returns: row where list of lessons end as Int
def _skip_lessons(sheet, start_row, end_row):
    spacer = 1 # empty rows between lessons and next class name
    for row in range(start_row, end_row):
        cell = sheet.cell(row=row, column=1)
        if(cell.value is None and row != end_row):
            return (row + spacer)
    return end_row

# executes functions
# returns class names as list
def run(class_filter = ""):
    filePath = _initiate_file()
    workbook = openpyxl.load_workbook(filePath)
    sheet=workbook.active
    classes = _get_classes_from_file(sheet=sheet, start_row=1, class_filter=class_filter)
    #print(classes)
    return classes

run()