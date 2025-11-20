


function buildTable(data) {
    let table = document.getElementById('detailBody');

    for (let i = 0; i < data.length; i++) {
        let row = `<tr>
                        <td>${data[i].fname}</td>
                        <td>${data[i].age}</td>
                        <td>${data[i].birthday}</td>
                   </tr>`
        table.innerHTML += row
    }   
}

buildTable(testArray);                         