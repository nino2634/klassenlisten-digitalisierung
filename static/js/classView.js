const userData = JSON.parse(sessionStorage.getItem('userData')).state
console.log(userData)

if (userData === "teacher"){
    const tableBody = document.getElementById('tableBody');

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

    observer.observe(tableBody, { childList: true, subtree: true });
}
