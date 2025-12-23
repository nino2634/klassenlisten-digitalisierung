import {getClassList, searchClass} from "./getClassList.js";
import {API_BASE_URL} from "./config.js";

const userData = JSON.parse(sessionStorage.getItem('userData')).state

document.addEventListener('DOMContentLoaded', async function () {
    await getClassList();
    searchClass();
    // Test: Muss dann auf lusd geändert werden
    if (userData === "teacher") {
        const tableTd = document.querySelectorAll('.tdBtn')
        tableTd.forEach(el => {
            const div = document.createElement('div')
            const checkbox = document.createElement('input')

            el.firstElementChild.className = 'col-12 col-sm-12 col-md-8 col-lg-10'


            div.className = 'form-check col-12 col-sm-12 col-md-4 col-lg-2 d-flex align-items-center justify-content-center';

            checkbox.className = 'form-check-input checkbox-item'
            checkbox.setAttribute('type','checkbox')
            checkbox.setAttribute('disabled','disabled')

            // Listener direkt hinzufügen
            checkbox.addEventListener('change', () => {
                const checkboxState = checkbox.checked;
                const className = el.firstElementChild.innerText
                const savedHalfYear = sessionStorage.getItem('selectedHalfYear');
                saveProgressState(checkboxState, className, savedHalfYear)
                getProgressState(savedHalfYear)
            })
            div.appendChild(checkbox)
            el.appendChild(div)
            async function saveProgressState(checkboxState, className, savedHalfYear) {
                try {
                    const response = await fetch(`${API_BASE_URL}/api/save_progress`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        credentials: 'include',
                        body: JSON.stringify({checkboxState, className, savedHalfYear})
                    });

                    if (!response.ok) {
                        // Erfolgreich → Weiterleitung
                        console.error('Fehler bei der Speicherung des Checkbox Status')

                    }

                } catch(error){
                    console.error(error)
                }
            }
            async function getProgressState(savedHalfYear) {
                try {
                    const response = await fetch(`${API_BASE_URL}/api/load_progress`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        credentials: 'include',
                        body: JSON.stringify({ savedHalfYear })
                    });

                    if (!response.ok) {
                        console.error('Fehler bei der Speicherung des Checkbox-Status');
                        return; // Beende die Funktion, wenn ein Fehler auftritt
                    }

                    const data = await response.json();
                    console.log('Erfolg:', data);

                    // Hier kannst du bei Erfolg weiterleiten oder andere Aktionen ausführen
                    // z.B.: window.location.href = '/next-page';

                } catch (error) {
                    console.error('Netzwerk- oder Parsing-Fehler:', error);
                }
            }

        });

    }
});
if (userData === 'teacher') {
    const dropdownItems = document.querySelectorAll('#halfYearDropdown .dropdown-item');

    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            // Alle Checkboxen holen
            const tableTd = document.querySelectorAll('.tdBtn');
            // Wert aus dem data-Attribut
            const value = item.dataset.value;

            tableTd.forEach(el => {
                const checkbox = el.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    // Deaktivieren, wenn value === "0", sonst aktivieren
                    checkbox.disabled = (value === "0");
                }
            });
        });
    });


}