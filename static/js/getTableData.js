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


function renderTable(data) {
    const tableBody = document.getElementById("myTableBody");
    tableBody.innerHTML = "";

    data.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.id}</td>
            <td>${row.name}</td>
        `;
        tableBody.appendChild(tr);
    });
}
      
