import { API_BASE_URL } from './config.js';
document.addEventListener('DOMContentLoaded', function() {
    const dropdownItems = document.querySelectorAll('#halfYearDropdown .dropdown-item');

    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            const half_year = this.dataset.value;
            const btn = document.getElementById('halfYearButton');
            btn.textContent = this.textContent;
            btn.dataset.value = half_year;
            dropdownItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

        });
    });

});

export async function getTeacherDetailedData(class_name, half_year){
    if (half_year === '1.Hj' || half_year === '2.Hj'){
        try{
            const response = await fetch(
                `${API_BASE_URL}/teacherDetailed?class_name=${encodeURIComponent(class_name)}&half_year=${encodeURIComponent(half_year)}`);
            const data = await response.json();
            console.log("Response OK:", response.ok);
            console.log("Response status:", response.status);
            console.log("Received data:", data);
            renderTableDetailed(data);
        } catch (error) {
            console.error("Fehler beim Laden:", error);
        }
    } else {
    showAlert("❌ Bitte zuerst das Halbjahr auswählen.");
    }

}

document.addEventListener('DOMContentLoaded', function() {
    const classList = document.querySelectorAll(".classList");
    classList.forEach(item => {
        item.addEventListener("click", function() {
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
    });
});

function renderTableDetailed(data) {
    const tbody = document.getElementById("detailBody");
    if (!tbody) {
        console.error("❌ Element #detailBody nicht gefunden.");
        return;
    }
    tbody.innerHTML = ""; // reset table


    const lessons = data.lessons || [];
    let sumSuS = 0;
    let sumKuk = 0;

    lessons.forEach((lesson, index) => {
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

    // Summenzeile
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


