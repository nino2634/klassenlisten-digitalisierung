import { API_BASE_URL } from './config.js';
document.addEventListener('DOMContentLoaded', async function () {
        await getClassList();
    }
);

async function getClassList() {
    try {
        const param = "";
        const response = await fetch(`${API_BASE_URL}/api/classes?classList=`+ encodeURIComponent(param));
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Fehler beim Laden:", error);
    }
}


