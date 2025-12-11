import { API_BASE_URL } from './config.js';
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Verhindert das normale Neuladen der Seite

        const user = document.getElementById('user').value;
        const password = document.getElementById('pass').value;

        try {
            const response = await fetch(`${API_BASE_URL}/api/verify_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ user, password })
            });

            const data = await response.json();
            console.log(data);

            if (response.ok && data.redirect_url) {
                // Erfolgreich → Weiterleitung
                window.location.href = data.redirect_url;

            } else {
                console.log("Fehler")
            }

        } catch (error) {
            console.error('Fehler beim Senden:', error);
            alert('⚠️ Server nicht erreichbar');
        }
    });
});