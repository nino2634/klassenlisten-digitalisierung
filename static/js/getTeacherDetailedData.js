import { API_BASE_URL } from './config.js';
document.addEventListener('DOMContentLoaded', function() {
    const dropdownItems = document.querySelectorAll('#halfYearDropdown .dropdown-item');

    dropdownItems.forEach(item => {
        item.addEventListener('click', function(event) {
            // Setzt das ausgewählte Item als Button-Text
            let half_year = document.getElementById('halfYearButton').textContent = this.textContent;

            // active-Klasse setzen
            dropdownItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            async function getTeacherDetailedData(class_name, half_year){
                try{
                    const response = await fetch(`${API_BASE_URL}/api/teacherDetailed=`+ encodeURIComponent(class_name) + encodeURIComponent(half_year));
                    const data = await response.json();
                    renderTableDetailed(data);
                } catch (error) {
                    console.error("Fehler beim Laden:", error);
                }
            }
            function renderTableDetailed(data){
                const tableBody = document.getElementById("tableBody");
                tableBody.innerHTML = "";
                data.forEach(row => {
                    const tr = document.createElement("tr");
                    tr.className = "border-0"
                    tr.innerHTML = `
                    <td class="p-0 m-1 border-0">
                    </td>`;
                    tableBody.appendChild(tr);
                });
            }
        });
    });
});




