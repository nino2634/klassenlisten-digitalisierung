import sys
import openpyxl

try:
    filter = sys.argv[1]
except IndexError:
    filter = ""

def get_classes_from_file(sheet, start_row): 
    classes = []
    spacer = 3 # empty rows between class name and lessons
    end_row = int(sheet.max_row)
    row:int = start_row
    while end_row > row:
        cell = sheet.cell(row=row, column=1)
        if cell.value is not None:
            print(cell.value)
            classes.append(cell.value)
            if(row+spacer < end_row):
                new_row=skip_lessons(sheet=sheet, start_row=row+spacer, end_row=end_row)
                row = new_row
            else:
                break;
        else:
            row += 1
    return classes

def skip_lessons(sheet, start_row, end_row):
    spacer = 1 # empty rows between lessons and next class name
    for row in range(start_row, end_row):
        cell = sheet.cell(row=row, column=1)
        #print(cell.value)
        if(cell.value is None and row != end_row):
            return (row + spacer)
        else:
            return end_row

def run():
    filePath = "src/app/data/Datenquelle.xlsx"
    workbook = openpyxl.load_workbook(filePath)
    sheet=workbook.active
    classes = get_classes_from_file(sheet=sheet, start_row=1)
    print(classes)

run()