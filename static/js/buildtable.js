function buildTable(data) {
    let table = document.getElementById('detailBody');

    for (let i = 0; i < data.length; i++) {
        let row = `<tr>  
                    <td>${data[i].name}</td>
                    <td>${data[i].age}</td>
                    <td>${data[i].birthdate}</td>
                    <td><div class="form-check">
                        <input class="form-check-input" type="checkbox" id="flexCheckDefault${i}">
                        <label class="form-check-label" for="flexCheckDefault${i}">fertig</label>
                        </div>
                    </td>
                    </tr>`;
        table.innerHTML += row
    }   
}

