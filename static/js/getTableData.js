document.addEventListener('DOMContentLoaded', async function() {
    await getTableData();
}
);

async function getTableData() {
try {
    const param = "";
    const response = await fetch('http://10.49.128.174:5000/api/classes?school_classes='+ encodeURIComponent(param)); 
    const data = await response.json();
    renderTable(data);
} catch (error) {
    console.error("Fehler beim Laden:", error);
}
}

let half_year = ""
function renderTable(data) {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = "";

    data.forEach(row => {
        const tr = document.createElement("tr");
        tr.className = "border-0"
        tr.innerHTML = `
            <td class="p-0 m-1 border-0"><button class="w-100 btn btn-primary tableButton rounded-0 m-0 border-0" onclick="getTeacherDetailedData(${row},half_year)">${row}</button></td>
        `;
        tableBody.appendChild(tr);
    });
}
      
