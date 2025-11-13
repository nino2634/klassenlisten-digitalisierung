// Export-Funktion: sichtbare Zeilen als CSV exportieren
document.getElementById('exportBtn').addEventListener('click', function() {
  const rows = Array.from(document.querySelectorAll('tbody tr'))
    .filter(r => r.offsetParent !== null) // nur sichtbare
    .map(r => '"' + r.querySelector('td').textContent.trim().replace(/"/g, '""') + '"');

  if (rows.length === 0) {
    alert('Keine Daten zum Exportieren.');
    return;
  }

  const csv = 'Klasse\n' + rows.join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'klassen.csv';
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

// Suchfunktion: filtert Tabellenzeilen
document.getElementById('searchInput').addEventListener('input', function() {
  const q = this.value.trim().toLowerCase();
  document.querySelectorAll('tbody tr').forEach(tr => {
    const txt = tr.textContent.trim().toLowerCase();
    tr.style.display = q === '' || txt.includes(q) ? '' : 'none';
  });
});
