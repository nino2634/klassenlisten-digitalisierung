import { getTeacherDetailedData } from './getTeacherDetailedData.js';

document.addEventListener("DOMContentLoaded", async () => {
    const tbody = document.getElementById("detailBody");
    if (!tbody) {
        console.error("❌ #detailBody existiert nicht im DOM. Script nur auf Detailseite laden!");
        return;
    }

    // URL-Parameter holen
    const params = new URLSearchParams(window.location.search);
    const class_name = params.get("class_name");
    const half_year = params.get("half_year");

    if (!class_name || !half_year) {
        console.error("❌ Fehlende Parameter in der URL.");
        return;
    }

    try {
        const data = await getTeacherDetailedData(class_name, half_year);
        renderTableDetailed(data);
    } catch (err) {
        console.error("Fehler beim Laden der Detaildaten:", err);
    }
});

function renderTableDetailed(data) {
    const tbody = document.getElementById("detailBody");
    if (!tbody) return;

    tbody.innerHTML = "";

    (data.lessons || []).forEach((lesson, index) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${lesson.Fach}</td>
            <td>${lesson.WoStd_SuS}</td>
            <td>${lesson.Lehrer}</td>
            <td>${lesson.WoStd_KuK}</td>
            <td class="text-wrap overflow-auto">
              <textarea class="auto-grow"
                        data-toggle="tooltip"
                        data-placement="top"
                        rows="1">${lesson.comment || ""}</textarea>
            </td>
        `;
        tbody.appendChild(tr);
    });

    const sumRow = document.createElement("tr");
    sumRow.innerHTML = `
        <td></td>
        <td>Summe:</td>
        <td id="sumSchueler">${data.Sum_SuS}</td>
        <td>Summe:</td>
        <td id="sumLehrer">${data.Sum_KuK}</td>
        <td></td>
    `;
    tbody.appendChild(sumRow);

    // Auto-Grow für alle gerade erzeugten Textareas aktivieren
    tbody.querySelectorAll('.auto-grow').forEach(function(textarea) {
        textarea.style.overflow = 'hidden';
        textarea.style.resize = 'none';

        const adjustHeight = (el) => {
            el.style.height = 'auto';
            el.style.height = el.scrollHeight + 'px';
        }

        adjustHeight(textarea);
        textarea.addEventListener('input', () => adjustHeight(textarea));
    });
}

async function exportExcel() {
    const table = document.getElementById("lessons_table");
    const rows = Array.from(table.tBodies[0].rows);

    const data = rows.map(row => ({
        nr: row.cells[0].innerText,
        fach: row.cells[1].innerText,
        stunden_schueler: row.cells[2].innerText,
        lehrer: row.cells[3].innerText,
        stunden_lehrer: row.cells[4].innerText,
        bemerkung: row.cells[5].querySelector('input')?.value || ''
    }));
    const response = await fetch("/api/export", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        alert("Export fehlgeschlagen");
        return;
    }

    // 🔽 Datei-Download erzwingen
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "export.xlsx";
    document.body.appendChild(a);
    a.click();

    a.remove();
    window.URL.revokeObjectURL(url);

    // Modal schließen
    const modalEl = document.getElementById('exportModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();
}

function exportPDF() {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF("landscape", "mm", "a4");

    const rows = [];
    const tableRows = document.querySelectorAll("#detailBody tr");

    tableRows.forEach(tr => {
        const cells = tr.querySelectorAll("td");
        if (cells.length === 0) return;

        rows.push([
            cells[0]?.innerText || "",
            cells[1]?.innerText || "",
            cells[2]?.innerText || "",
            cells[3]?.innerText || "",
            cells[4]?.innerText || "",
            cells[5]?.querySelector("textarea")?.value || cells[5]?.innerText || ""
        ]);
    });

    pdf.autoTable({
        startY: 40,
        head: [[
            "Nr.",
            "Fach",
            "Std./SuS",
            "Lehrer",
            "Std./KuK",
            "Bemerkung"
        ]],
        body: rows,

        theme: "grid", // 🔑 Gitter überall

        headStyles: {
            fillColor: '#29235c', // weiß
            textColor: '#ffffff',
            lineWidth: 0.2
        },

        styles: {
            fontSize: 9,
            cellPadding: 3,
            valign: "top",
            lineWidth: 0.1,        // Linienbreite
            lineColor: [0, 0, 0]   // schwarz
        },

        columnStyles: {
            5: { cellWidth: 80 }
        },
        // Gerade Zeilen einfärben
        didParseCell: function (data) {
            if (data.section === 'body' && data.row.index % 2 === 1) {
                data.cell.styles.fillColor = [200, 230, 250]; // RGB
                data.cell.styles.fillOpacity = 0.1; // entspricht 71 in Hex (71/255 ≈ 0.278)
            }
        }
    });


    pdf.save("export.pdf");
}

window.exportPDF = exportPDF;
window.exportExcel = exportExcel;
