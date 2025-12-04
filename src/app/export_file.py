from openpyxl import Workbook
from pathlib import Path
import tempfile

def export_file(table, class_name):
    # OS-unabhängiges temp-Verzeichnis
    temp_dir = Path(tempfile.gettempdir())

    # Speicherdatei (z.B. /tmp/02TSFR_klassenliste.xlsx)
    output_file = temp_dir / f"{class_name}_klassenliste.xlsx"

    wb = Workbook()
    ws = wb.active

    # Header
    ws.append(list(table[0].keys()))

    # Rows
    for row in table:
        ws.append(list(row.values()))

    wb.save(output_file)

    # Rückgabe: absoluter Pfad als String
    return str(output_file)
