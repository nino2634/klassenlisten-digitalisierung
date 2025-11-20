// Export sichtbarer Zeilen als CSV
document.getElementById('exportBtn').addEventListener('click', function(){
  const rows = Array.from(document.querySelectorAll('#detailBody tr'))
    .map(tr => Array.from(tr.children).map(td => td.textContent.trim().replace(/"/g,'""')))
    .map(cols => '"' + cols.join('","') + '"');
  if(!rows.length){ alert('Keine Daten zum Exportieren.'); return; }

  const header = ['Nr.','Fach/Lernfeld','Stunden/Woche Schüler','Lehrer','Stunden/Woche Lehrer','Form','Bemerkung'];
  const csv = '"' + header.join('","') + '"\n' + rows.join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'lusd_klassen_detailliert.csv'; document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
});

// Platzhalter für Abbrechen/Fertig
document.getElementById('cancelBtn').addEventListener('click', () => {
  window.history.back(); // oder z.B. window.location.href = '../seite2/index.html';
});

document.getElementById('doneBtn').addEventListener('click', () => {
  alert('Änderungen gespeichert!');
});
