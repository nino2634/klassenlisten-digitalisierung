import { API_BASE_URL } from './config.js';
import { getTeacherDetailedData } from './getTeacherDetailedData.js';
document.addEventListener('DOMContentLoaded', async function() {
    await getTableData();
}
);

async function getTableData() {
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

      
