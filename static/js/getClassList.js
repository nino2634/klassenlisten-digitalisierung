import { API_BASE_URL } from './config.js';
import { getTeacherDetailedData } from './getTeacherDetailedData.js';
document.addEventListener('DOMContentLoaded', async function() {
    await getClassList();
}
);

async function getClassList() {
try {
    const param = "";
    const response = await fetch(`${API_BASE_URL}/api/classes?school_classes=`+ encodeURIComponent(param));
    const data = await response.json();
    renderTable(data);
} catch (error) {
    console.error("Fehler beim Laden:", error);
}
}

function renderTable(data) {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = "";

    data.forEach(row => {
        const tr = document.createElement("tr");
        tr.className = "border-0";

        const td = document.createElement("td");
        td.className = "p-0 m-1 border-0";

        const btn = document.createElement("button");
        btn.className = "w-100 btn btn-primary tableButton rounded-0 m-0 border-0 classList";
        btn.textContent = row;

        // Event Listener direkt hier setzen
        btn.addEventListener("click", function() {
            const class_name = this.textContent.trim();
            const half_year = document.getElementById('halfYearButton').dataset.value;
            getTeacherDetailedData(class_name, half_year);

        });


        td.appendChild(btn);
        tr.appendChild(td);
        tableBody.appendChild(tr);
    });
}

/*
document.addEventListener("DOMContentLoaded", function () {
    const searchBtn = document.getElementById("searchBtn");
    const searchInput = document.querySelector("#searchForm #searchInput");
    const tableBody = document.getElementById("tableBody");

    searchBtn.addEventListener("click", function (e) {
        e.preventDefault();

        const filter = searchInput.value.trim().toLowerCase();
        const rows = document.querySelectorAll("#tableBody tr");
        let visibleCount = 0;

        // Existierende "keine Treffer"-Zeile entfernen (falls vorhanden)
        const noRow = document.getElementById("noResultsRow");
        if (noRow) noRow.remove();

        // Filtern
        rows.forEach(row => {
            const btn = row.querySelector("button.classList");
            const className = btn.textContent.trim().toLowerCase();

            if (filter === "" || className.includes(filter)) {
                row.classList.remove("d-none");
                visibleCount++;
            } else {
                row.classList.add("d-none");
            }
        });

        // Wenn keine Zeile sichtbar → neue einfügen
        if (visibleCount === 0) {
            const tr = document.createElement("tr");
            tr.id = "noResultsRow";

            const td = document.createElement("td");
            td.className = "text-center text-muted py-3";
            td.textContent = "Keine Klassen gefunden";

            tr.appendChild(td);
            tableBody.appendChild(tr);
        }
    });
}); 
*/

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector("#searchForm #searchInput");
    const tableBody = document.getElementById("tableBody");

    function filterRows() {
        const filter = searchInput.value.trim().toLowerCase();
        const rows = document.querySelectorAll("#tableBody tr");
        let visibleCount = 0;

        // "Keine Treffer" Zeile entfernen, falls vorhanden
        const noRow = document.getElementById("noResultsRow");
        if (noRow) noRow.remove();

        rows.forEach(row => {
            const btn = row.querySelector("button.classList");
            const className = btn.textContent.trim().toLowerCase();

            if (filter === "" || className.includes(filter)) {
                row.classList.remove("d-none");
                visibleCount++;
            } else {
                row.classList.add("d-none");
            }
        });

        // Wenn keine übrig → Meldungszeile einfügen
        if (visibleCount === 0) {
            const tr = document.createElement("tr");
            tr.id = "noResultsRow";

            const td = document.createElement("td");
            td.className = "text-center text-muted py-3";
            td.textContent = "Keine Klassen gefunden";

            tr.appendChild(td);
            tableBody.appendChild(tr);
        }
    }

    // 👇 Live-Suche: wird bei JEDER Eingabe ausgelöst
    searchInput.addEventListener("input", filterRows);
});
