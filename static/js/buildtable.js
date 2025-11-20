
var myArray = [
	    {'name':'KlasseA', 'age':'MAthe', 'birthdate':'11/10/1989'},
	    {'name':'KLasseA', 'age':'Deutsch', 'birthdate':'10/1/1989'},
	    {'name':'Paul', 'age':'29', 'birthdate':'10/14/1990'},
	    {'name':'Dennis', 'age':'25', 'birthdate':'11/29/1993'},
	    {'name':'Tim', 'age':'27', 'birthdate':'3/12/1991'},
	    {'name':'Erik', 'age':'24', 'birthdate':'10/31/1995'},
	]
    
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