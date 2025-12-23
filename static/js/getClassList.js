import { API_BASE_URL } from './config.js';

export async function getClassList() {
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

        const div = document.createElement("div");
        div.classList = "row tdBtn px-0 mx-0";
        const divBtn = document.createElement("div");

        const btn = document.createElement("button");
        btn.className = "w-100 btn btn-primary tableButton rounded-0 m-0 border-0 classList my-fs";
        btn.textContent = row;
        divBtn.appendChild(btn);
        div.appendChild(divBtn)
        td.appendChild(div);
        tr.appendChild(td);
        tableBody.appendChild(tr);
    });
}

export function searchClass(){
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

        // Wenn keine Klassen gefunden wurden → Meldungszeile einfügen
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

    searchInput.addEventListener("input", filterRows);
}

