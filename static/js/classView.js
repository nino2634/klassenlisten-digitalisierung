import {getClassList, searchClass} from "./getClassList.js";

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

            el.firstElementChild.classList.add('col-10')
            /*el.classList.add('row')*/

            div.className = 'form-check col-2 d-flex align-items-center justify-content-center';

            checkbox.classList.add('form-check-input')
            checkbox.setAttribute('type','checkbox')
            checkbox.setAttribute('disabled','disabled')
            div.appendChild(checkbox)
            el.appendChild(div)
        })
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


/*<div className="form-check">
    <input className="form-check-input" type="checkbox" value="" id="flexCheckDefault"/>
    <label className="form-check-label" htmlFor="flexCheckDefault">
        Default checkbox
    </label>
</div>*/

/*
    const observer = new MutationObserver((mutationsList) => {
        mutationsList.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                console.log(node.querySelector('.tdBtn'))
                const nodeElements = node.querySelector('.tdBtn')
                nodeElements.classList.add('row')
                nodeElements.firstElementChild.classList.add('col-9')
                const div = document.createElement('div')
                div.classList.add('col-3')
                nodeElements.appendChild(div)

            });
        });
    });

    observer.observe(tableBody, { childList: true, subtree: true });*/
/*}*/
