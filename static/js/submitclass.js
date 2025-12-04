import { API_BASE_URL } from './config.js';
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('searchForm');
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Verhindert das normale Neuladen der Seite

        
            try {
            const response = await fetch(`${API_BASE_URL}/api/placeholder`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({form})
            });

            const data = await response.json();
            console.log(data);


        } catch (error) {
            console.error('Fehler beim Senden:', error);
            alert('⚠️ Server nicht erreichbar');
        }
    });
});