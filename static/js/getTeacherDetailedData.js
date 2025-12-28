import {API_BASE_URL} from './config.js';
//Halbjahr Dropdown Listener
document.addEventListener('DOMContentLoaded', function() {
    const dropdownItems = document.querySelectorAll('#halfYearDropdown .dropdown-item');

    // Gespeicherten Wert wiederherstellen, falls vorhanden
    const savedHalfYear = sessionStorage.getItem('selectedHalfYear');
    if (savedHalfYear) {
        const btn = document.getElementById('halfYearButton');
        const matchingItem = Array.from(dropdownItems).find(item => item.dataset.value === savedHalfYear);
        if (matchingItem) {
            btn.textContent = matchingItem.textContent;
            btn.dataset.value = savedHalfYear;
            dropdownItems.forEach(i => i.classList.remove('active'));
            matchingItem.classList.add('active');
        }
    }

    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            const half_year = this.dataset.value;
            const btn = document.getElementById('halfYearButton');
            btn.textContent = this.textContent;
            btn.dataset.value = half_year;
            dropdownItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            // In Session speichern
            sessionStorage.setItem('selectedHalfYear', half_year);
        });
    });
});

// Klassenliste Listener
document.addEventListener("click", function(e) {
    if (e.target.classList.contains("classList")) {
        const class_name = e.target.textContent.trim();
        const half_year = document.getElementById('halfYearButton').dataset.value;
        console.log("Weitergeleitet!", class_name, half_year);
        if(half_year === "1.Hj" || half_year === "2.Hj"){
            window.location.href = `/classViewDetailed?class_name=${encodeURIComponent(class_name)}&half_year=${encodeURIComponent(half_year)}`;
        }else{
            showAlert("❌ Bitte zuerst das Halbjahr auswählen!")
        }
    }
});

export async function getTeacherDetailedData(class_name, half_year) {
    console.log("klasse: " + class_name + " halbjahr: " + half_year);
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/classViewDetailed?class_name=${encodeURIComponent(class_name)}&half_year=${encodeURIComponent(half_year)}`
        );

        if (!response.ok) {
            // HTTP-Fehler behandeln
            throw new Error(`Fehler beim Laden: ${response.status} ${response.statusText}`);
        }

        const data = await response.json(); // immer JSON parsen
        return data;

    } catch (error) {
        console.error("Fehler beim Laden:", error);
        throw error; // damit der Aufrufer weiß, dass etwas schiefging
    }
}





