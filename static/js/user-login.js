document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Verhindert das normale Neuladen der Seite

        const user = document.getElementById('user').value;
        const password = document.getElementById('pass').value;

        try {
            const response = await fetch('http://10.49.128.174:5000/api/verify_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user, password })
            });

            const data = await response.json();
            console.log(data);

            if (response.ok) {
                alert('✅ Erfolgreich eingeloggt!');
            } else {
                alert('❌ Login fehlgeschlagen: ' + (data.message || 'Unbekannter Fehler'));
            }

        } catch (error) {
            console.error('Fehler beim Senden:', error);
            alert('⚠️ Server nicht erreichbar');
        }
    });
});