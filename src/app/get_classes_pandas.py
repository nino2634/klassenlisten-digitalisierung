import pandas as pd
import json
from .config.config_handler import load_config_data
from .get_headers import run as get_headers

def run(class_filter=""):
    file=load_config_data("excel_file") 
    # Pandas DataFrame laden
    df = pd.read_excel(file, header=None)

    # Erste Spalte extrahieren
    first_col = df.iloc[:, 0]

    # Header-Liste aus deinem Helper
    headers = json.loads(get_headers())

    # Filtern: nur Strings, Filter enthalten, nicht in headers
    classes = (
        first_col[first_col.apply(lambda x: isinstance(x, str))]
        .loc[lambda s: s.str.contains(class_filter)]
        .loc[lambda s: ~s.str.strip().isin(headers)]
        .tolist()
    )

    if not classes:
        return json.dumps(f"Class '{class_filter}' not found")

    return json.dumps(classes)

result = run("")
print(result)