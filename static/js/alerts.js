function showAlert(message, type = "danger", timeout = 5) {
    // Direkt ans Ende des body anhängen
    const container = document.body;

    const alert = document.createElement("div");
    alert.className = `alert alert-${type} d-flex align-items-center mb-0 rounded-0 position-fixed`;
    alert.style.top = "0";
    alert.style.left = "0";
    alert.style.width = "100%";
    alert.style.zIndex = "12000"; // über allen Modals
    alert.role = "alert";
    alert.innerHTML = `
        <svg class="bi flex-shrink-0 me-2" role="img" aria-label="${type}:" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor">
            <use xlink:href="#exclamation-triangle-fill"/>
        </svg>
        <div>${message}</div>
    `;

    container.appendChild(alert);

    setTimeout(() => {
        alert.remove();
    }, timeout * 1000);
}
