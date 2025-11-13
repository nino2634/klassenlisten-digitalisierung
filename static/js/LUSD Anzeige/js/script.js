// Export sichtbarer Zeilen als CSV
document.getElementById('exportBtn').addEventListener('click', function(){
  const rows = Array.from(document.querySelectorAll('#classBody tr'))
    .filter(r => r.style.display !== 'none')
    .map(r => {
      const cols = Array.from(r.children).map(td => td.textContent.trim().replace(/"/g,'""'));
      return '"' + cols.join('","') + '"';
    });
  if(!rows.length){ alert('Keine sichtbaren Einträge zum Exportieren.'); return; }
  const csv = '"Klasse","Bearbeitungsstatus"\n' + rows.join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'klassen.csv'; document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
});

// Live-Suche
document.getElementById('searchInput').addEventListener('input', function(){
  const q = this.value.trim().toLowerCase();
  document.querySelectorAll('#classBody tr').forEach(tr=>{
    const txt = tr.textContent.toLowerCase();
    tr.style.display = q === '' || txt.includes(q) ? '' : 'none';
  });
});

// Status-Toggle: zyklisch filtern nach Bearbeitungsstatus
(function(){
  const states = ['all','unbearbeitet','bearbeitet'];
  let idx = 0;
  const btn = document.getElementById('statusToggle');
  function apply(s){
    document.querySelectorAll('#classBody tr').forEach(tr=>{
      const st = tr.children[1].textContent.trim().toLowerCase();
      tr.style.display = (s === 'all' || st === s) ? '' : 'none';
    });
    const labels = {
      all: 'Alle anzeigen',
      unbearbeitet: 'Nur unbearbeitet',
      bearbeitet: 'Nur bearbeitet'
    };
    btn.textContent = labels[s];
  }
  btn.addEventListener('click', function(){
    idx = (idx + 1) % states.length;
    apply(states[idx]);
  });
  apply(states[idx]);
})();
