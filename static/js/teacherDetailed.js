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

    console.log("Tabelle erfolgreich aktualisiert.");
}

