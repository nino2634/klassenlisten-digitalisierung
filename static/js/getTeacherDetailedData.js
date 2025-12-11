import { API_BASE_URL } from './config.js';
document.addEventListener('DOMContentLoaded', function() {
    const dropdownItems = document.querySelectorAll('#halfYearDropdown .dropdown-item');

    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            const half_year = this.dataset.value; // "1" oder "2"
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

            renderTableDetailed(response, class_name, half_year);

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
            console.log(typeof class_name)
            const half_year = document.getElementById('halfYearButton').dataset.value;
            if (half_year === '1.Hj' || half_year === '2.Hj'){
                getTeacherDetailedData(class_name, half_year);
            } else{
                showAlert("❌ Bitte zuerst das Halbjahr auswählen.");
            }

        });
    });
});

function renderTableDetailed(response, class_name, half_year) {
    if ((half_year === '1.Hj' || half_year === '2.Hj')) {
        // Erfolgreich → Weiterleitung
        window.location.href = `/teacherDetailed?class_name=${class_name}&half_year=${half_year}`;
    } else {
        // Login fehlgeschlagen
        showAlert("❌ Serverfehler - Daten konnten nicht abgerufen werden");
        }
}

