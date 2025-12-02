document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', function () {
        // Button-Text ändern
        document.getElementById('halfYearButton').textContent = this.textContent;

        // Optional: aktive Klasse setzen
        document.querySelectorAll('.dropdown-item').forEach(i => i.classList.remove('active'));
        this.classList.add('active');
    });
});