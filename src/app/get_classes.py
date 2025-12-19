import pandas as pd
import json
from .config.config_handler import load_config_data
from .get_headers import run as get_headers

def run(class_filter):
    """
    Sucht in Spalte 1 des Worksheets nach Klassennamen, die den class_filter enthalten
    
    :param class_filter: String, Filter für Klassennamen
    
    returns: JSON-encoded Liste der gefundenen Klassennamen oder eine Fehlermeldung
    """
    file=load_config_data("excel_file") 
    # Pandas DataFrame laden
    df = pd.read_excel(file, header=None)

    # Erste Spalte extrahieren
    first_col = df.iloc[:, 0]

    # Header-Liste laden
    headers = json.loads(get_headers())

    classes = (
        first_col[first_col.apply(lambda x: isinstance(x, str))] #nur strings
        .loc[lambda s: s.str.contains(class_filter)] #filter prüfen
        .loc[lambda s: ~s.str.strip().isin(headers)] #nicht in headers
        .tolist()
    )

    if not classes:
        return json.dumps(f"Class '{class_filter}' not found")

    return json.dumps(classes)

#result = run("")
#print(result)