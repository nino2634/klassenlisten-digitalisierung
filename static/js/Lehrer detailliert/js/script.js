// Export-Funktion: CSV aus sichtbarer Tabelle erstellen
document.getElementById('exportBtn').addEventListener('click', function() {
  const rows = Array.from(document.querySelectorAll('#detailBody tr'))
    .map(tr => Array.from(tr.children).map(td => td.textContent.trim().replace(/"/g, '""')))
    .map(cols => '"' + cols.join('","') + '"');
  
  if (rows.length === 0) {
    alert('Keine Daten zum Exportieren.');
    return;
  }

  const header = ['Nr.', 'Fach/Lernfeld', 'Stunden/Woche Schüler', 'Lehrer', 'Stunden/Woche Lehrer', 'Form', 'Bemerkung'];
  const csv = '"' + header.join('","') + '"\n' + rows.join('\n');
  
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'klassen_detailliert.csv';
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

// "Zurück"-Button
document.getElementById('backBtn').addEventListener('click', function() {
  window.history.back();
});

// Summenberechnung
function updateSums() {
  const schueler = Array.from(document.querySelectorAll('#detailBody tr td:nth-child(3)'))
    .map(td => parseFloat(td.textContent) || 0);
  const lehrer = Array.from(document.querySelectorAll('#detailBody tr td:nth-child(5)'))
    .map(td => parseFloat(td.textContent) || 0);

  const sumSchueler = schueler.reduce((a, b) => a + b, 0);
  const sumLehrer = lehrer.reduce((a, b) => a + b, 0);

  document.getElementById('sumSchueler').textContent = `Summe: ${sumSchueler}`;
  document.getElementById('sumLehrer').textContent = `Summe: ${sumLehrer}`;
}

updateSums();
