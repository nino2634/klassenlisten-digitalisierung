import { API_BASE_URL } from './config.js';
document.addEventListener('DOMContentLoaded', function() {
    const dropdownItems = document.querySelectorAll('#halfYearDropdown .dropdown-item');

    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            const half_year = this.dataset.value; // "1" oder "2"
            const btn = document.getElementById('halfYearButton');
            btn.textContent = this.textContent;
            btn.dataset.value = half_year; // Speichern
            dropdownItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });


});


export async function getTeacherDetailedData(class_name, half_year){
    try{
        const response = await fetch(`${API_BASE_URL}/teacherDetailed?class_name=${encodeURIComponent(class_name)}&half_year=${encodeURIComponent(half_year)}`);
        renderTableDetailed(response, class_name, half_year);
    } catch (error) {
        console.error("Fehler beim Laden:", error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const classList = document.querySelectorAll(".classList");
    classList.forEach(item => {
        item.addEventListener("click", function() {
            const class_name = this.textContent.trim();
            console.log("ok " + class_name);
            const half_year = document.getElementById('halfYearButton').dataset.value;
            getTeacherDetailedData(class_name, half_year);

        });
    });
});

function renderTableDetailed(response, class_name, half_year) {
    if (response.ok) {
        // Erfolgreich → Weiterleitung
        window.location.href = `/teacherDetailed?class_name=${class_name}&half_year=${half_year}`;


    } else {
        // Login fehlgeschlagen
        if (data.status === "failed") {
            showAlert("❌ Login fehlgeschlagen: Ungültige Zugangsdaten");
        } else {
            showAlert("❌ Login fehlgeschlagen: Unbekannter Fehler");
        }
    }
}

