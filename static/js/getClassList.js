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

        // Event Listener setzen
        btn.addEventListener("click", function() {
            const class_name = this.textContent.trim();
            const half_year = document.getElementById('halfYearButton').dataset.value;
            
            if (half_year === '1.Hj' || half_year === '2.Hj') {
                // Speichern für Detailseite
                sessionStorage.setItem("class_name", class_name);
                sessionStorage.setItem("half_year", half_year);
                
                // Seitenwechsel
                window.location.href = "/teacherDetailed";
            } else {
                showAlert("❌ Bitte zuerst das Halbjahr auswählen.");
            }
        });


        td.appendChild(btn);
        tr.appendChild(td);
        tableBody.appendChild(tr);
    });
}

      
