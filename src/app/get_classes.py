import pandas as pd
import json
from .file_handler import initiate_file, get_next_row_with_value

def run(class_filter=""):
    # Excel-Datei laden (nur die erste Spalte)
    df = pd.read_excel(initiate_file, usecols=[0], engine="openpyxl")
    
    # Alle Werte in der ersten Spalte in Strings umwandeln (NaN → leere Strings)
    df.iloc[:, 0] = df.iloc[:, 0].astype(str)
    
    # Filtern nach class_filter
    if class_filter:
        filtered = df[df.iloc[:, 0].str.contains(class_filter, na=False)]
    else:
        filtered = df[df.iloc[:, 0] != '']  # Alle nicht-leeren Werte
    
    # In Liste umwandeln
    classes = filtered.iloc[:, 0].tolist()
    
    # Rückgabe
    if not classes:
        return json.dumps(f"Class '{class_filter}' not found")
    return json.dumps(classes)

#result = run("")  # Optionaler Filter
#print(result)