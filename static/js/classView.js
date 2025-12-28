import {getClassList, searchClass} from "./getClassList.js";
import {API_BASE_URL} from "./config.js";

const userData = JSON.parse(sessionStorage.getItem('userData')).state
const savedHalfYear = sessionStorage.getItem('selectedHalfYear');

document.addEventListener('DOMContentLoaded', async function () {
    await getClassList();
    searchClass();

    if (userData === "teacher") {
        const tableTd = document.querySelectorAll('.tdBtn');

        tableTd.forEach(el => {
            const div = document.createElement('div');
            const checkbox = document.createElement('input');

            el.firstElementChild.className = 'col-12 col-sm-12 col-md-8 col-lg-10';

            div.className = 'form-check col-12 col-sm-12 col-md-4 col-lg-2 d-flex align-items-center justify-content-center';

            checkbox.className = 'form-check-input checkbox-item';
            checkbox.setAttribute('type','checkbox');

            // Listener direkt hinzufügen
            checkbox.addEventListener('change', () => {
                const checkboxState = checkbox.checked;
                const className = el.firstElementChild.innerText;
                saveProgressState(checkboxState, className, savedHalfYear);
            });

            div.appendChild(checkbox);
            el.appendChild(div);
        });

        // Warten bis alle Checkboxen existieren dann → Status setzen
        const dropdownItems = document.querySelectorAll('#halfYearDropdown .dropdown-item');
        const value = sessionStorage.getItem('selectedHalfYear') || dropdownItems[0].dataset.value;
        updateCheckboxes(value);

        // EventListener für Dropdown
        dropdownItems.forEach(item => {
            item.addEventListener('click', function() {
                const value = item.dataset.value;
                sessionStorage.setItem('selectedHalfYear', value);
                updateCheckboxes(value);
            });
        });

        // Funktion auslagern
        function updateCheckboxes(value) {
            const tableTd = document.querySelectorAll('.tdBtn');
            tableTd.forEach(el => {
                const checkbox = el.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    checkbox.disabled = (value === "0");
                }
            });
        }

        // Progress speichern/abrufen
        async function saveProgressState(checkboxState, className, savedHalfYear) {
            try {
                const response = await fetch(`${API_BASE_URL}/api/save_progress`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ checkboxState, className, savedHalfYear })
                });
                if (!response.ok) console.error('Fehler bei der Speicherung des Checkbox Status');
            } catch(error) {
                console.error(error);
            }
        }

        async function getProgressState(savedHalfYear) {
            try {
                const response = await fetch(`${API_BASE_URL}/api/load_progress`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ savedHalfYear })
                });
                if (!response.ok) {
                    console.error('Fehler bei der Speicherung des Checkbox-Status');
                    return;
                }
                const data = await response.json();
                console.log('Meldung:', data);
            } catch (error) {
                console.error('Netzwerk- oder Parsing-Fehler:', error);
            }
        }
        await getProgressState(savedHalfYear);
    }
});
