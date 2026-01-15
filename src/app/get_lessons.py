# -*- coding: utf-8 -*-
import json
from .get_headers import run as get_headers
from .file_handler import initiate_file, get_next_empty_row, get_next_row_with_value
from .config.config_handler import load_config_data

# Spaltennamen aus settings.txt laden
# encode ist für Windows Kompatibilität notwendig, ansonsten gibt es Probleme mit Umlauten
classes_column_name = load_config_data("classes_column_name")
weekly_hrs_column_name = load_config_data("weekly_hrs_column_name")
half_year_column_name = load_config_data("half_year_column_name")#.encode("latin-1").decode("utf-8")
subject_column_name = load_config_data("subject_column_name")
teacher_column_name = load_config_data("teacher_column_name")

def _find_class_title_row(sheet, class_filter):
    """
    Sucht die erste Spalte des Worksheets nach dem Klassennamen ab ung gibt die Zeilennummer zurück 
    oder wirft eine Exception, wenn die Klasse nicht gefunden wurde.
    
    :param sheet: openpyxl Worksheet Objekt
    :param class_filter: String, Name der Klasse
    
    return: Integer, Zeilennummer der Klasse
    """
    end_row = sheet.max_row
    for row in range(1, end_row):
        cell = sheet.cell(row=row, column=sheet.min_column)
        if cell.value == class_filter:
            return row
    raise Exception("Class not found")
    
def _get_lessons_by_class(sheet, class_title, con_year_half, headers):
    """
    Nimmt alle Schulstunden einer Klasse aus dem Worksheet, formatiert sie und gibt sie als Liste von Dictionaries zurück.
    
    :param sheet: openpyxl Worksheet Objekt
    :param class_title: String, Name der Klasse
    :param con_year_half: String, Halbjahr, nach dem NICHT gesucht wird
    :param headers: list, Liste der Header-Namen
    
    returns: dict, Dictionary mit Klassenname, Liste der Schulstunden und Summen der Stunden
    """
    title_row = _find_class_title_row(sheet, class_title)
    row = get_next_row_with_value(sheet, title_row + 1) + 1 #zweite Zeile mit Inhalt nach der Titelzeile, erste sind header
    end_row = get_next_empty_row(sheet, row) #erste leere Zeile nach Start == Ende der Schulstunden

    start_col = sheet.min_column #erste Spalte im Worksheet mit Inhalt
    end_col = sheet.max_column #letzte Spalte im Worksheet mit Inhalt
    subject_column = headers.index(subject_column_name) + 1 #Spaltenindex des Fachs (1-basiert)

    lessons_list = []
    sum_sus = 0 # Summe aller Schüler-Wochenstunden
    sum_kuk = 0 # Summe aller Lehrer-Wochenstunden

    while row < end_row:
        lesson = {}
        mergeRows = False

        # nur Zeilen berücksichtigen, die nicht zum gegebenen Halbjahr gehören
        if con_year_half not in str(sheet.cell(row, headers.index(half_year_column_name) + 1).value):
            # Werte aus der Zeile auslesen
            for col in range(start_col, end_col):
                cell = sheet.cell(row, col)
                header = headers[col - 1]
                lesson[header] = f"{cell.value}"

                # Wochenstunden auf 0 setzen, wenn leer, sonst auf 3 Nachkommastellen runden
                if weekly_hrs_column_name in header and (cell.value is None or cell.value == 'None'):
                    lesson[header] = 0
                elif weekly_hrs_column_name in header and (cell.value is not None or cell.value != 'None'):
                    lesson[header] = str(cell.value)
                    
                # Wenn aktuelles Fach mehrfach in Liste vorkommt, dann Mergen aktivieren
                if headers[col - 1] == subject_column_name:
                    next_cell = sheet.cell(row + 1, col)
                    if cell.value == next_cell.value: 
                        mergeRows = True

            # Kommentar für gekoppelte Klassen
            if "," in lesson[classes_column_name]:
                classes = [c.strip() for c in lesson[classes_column_name].split(",")]
                comment = "gekoppelt mit"
                for class_name in classes:
                    if class_name != class_title:
                        comment += f" {class_name},"
                lesson['comment'] = comment.rstrip(",")

            # Merge-Logik
            nextRow = row + 1
            while mergeRows and nextRow < end_row:
                # Lehrer zusammenführen
                if sheet.cell(nextRow, headers.index(teacher_column_name) + 1).value not in lesson[teacher_column_name]:
                    lesson[teacher_column_name] += f", {sheet.cell(nextRow, headers.index(teacher_column_name) + 1).value}"
                    lesson[f"{weekly_hrs_column_name}_KuK"] = str(lesson[f"{weekly_hrs_column_name}_KuK"])
                    lesson[f"{weekly_hrs_column_name}_KuK"] += " - " + str(sheet.cell(nextRow, headers.index(f"{weekly_hrs_column_name}_KuK") + 1).value)
                
                # Nächste Zeile
                nextRow += 1

                # Abbruchbedingung: Ende erreicht oder Subject unterschiedlich
                if nextRow >= end_row or sheet.cell(nextRow, subject_column).value != sheet.cell(row, subject_column).value:
                    mergeRows = False

            # row auf nextRow setzen, damit äußere Schleife korrekt weiterläuft
            row = nextRow

            # Lesson zu Liste hinzufügen
            lessons_list.append(lesson)

            # Wochenstunden zu Summen addieren
            sum_sus += float(lesson[f"{weekly_hrs_column_name}_SuS"])
            if "-" in str(lesson[f"{weekly_hrs_column_name}_KuK"]):
                # Mehrere Lehrer, Stunden aufsplitten und addieren
                kuk_hours = [float(x.strip()) for x in lesson[f"{weekly_hrs_column_name}_KuK"].split("-")]
                sum_kuk += sum(kuk_hours)
            else:
                sum_kuk += float(lesson[f"{weekly_hrs_column_name}_KuK"])
        else:
            # Halbjahr passt nicht, einfach zur nächsten Zeile
            row += 1

    return {
        "class_name": f"{class_title}",
        "lessons": lessons_list,
        "Sum_SuS": sum_sus,
        "Sum_KuK": round(sum_kuk, 3) # auf 3 Nachkommastellen runden
    }

def run(class_title, year_half):
    """
    Methode zum Ausführen der Logik zum Abrufen der Schulstunden einer Klasse.
    
    :param class_title: String, Name der Klasse
    :param year_half: String, Halbjahr, nach dem gesucht wird
    
    returns: Liste mit Klassennamen, Liste der Stunden und Summe der Wochenstunden als json-Objekt
    """
    # Halbjahr tauschen
    # benötigt, da Stunden, die in beiden Halbjahren stattfinden, gar kein Halbjahr in der Spalte stehen haben
    con_year_half = year_half
    if "1.Hj" in year_half:
        con_year_half = str.replace(con_year_half, "1.Hj", "2.Hj")
    elif "2.Hj" in year_half:
        con_year_half = str.replace(con_year_half, "2.Hj", "1.Hj")
    
    workbook = initiate_file()
    sheet = workbook.active
    headers = json.loads(get_headers())
    lesson_list = _get_lessons_by_class(sheet, class_title, con_year_half, headers)  
    lesson_json = json.dumps(lesson_list)  
    return lesson_json

#result = run("02TSBR", "1.Hj")
#print(result)