import { getTeacherDetailedData } from './getTeacherDetailedData.js';

document.addEventListener("DOMContentLoaded", async () => {
    const tbody = document.getElementById("detailBody");
    if (!tbody) {
        console.error("❌ #detailBody existiert nicht im DOM. Script nur auf Detailseite laden!");
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
    if (!tbody) return; // <--- Prüft, ob DOM existiert

    tbody.innerHTML = "";

    let sumSuS = 0;
    let sumKuk = 0;

    (data.lessons || []).forEach((lesson, index) => {
        sumSuS += Number(lesson.WoStd_SuS);
        sumKuk += Number(lesson.WoStd_KuK);

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${lesson.Fach}</td>
            <td>${lesson.WoStd_SuS}</td>
            <td>${lesson.Lehrer}</td>
            <td>${lesson.WoStd_KuK}</td>
            <td><input type="text" value="${lesson.comment || ""}"></td>
        `;
        tbody.appendChild(tr);
    });

    const sumRow = document.createElement("tr");
    sumRow.innerHTML = `
        <td></td>
        <td>Summe:</td>
        <td id="sumSchueler">${sumSuS}</td>
        <td>Summe:</td>
        <td id="sumLehrer">${sumKuk}</td>
        <td></td>
    `;
    tbody.appendChild(sumRow);

    console.log("Tabelle erfolgreich aktualisiert.");
}
