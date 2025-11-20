document.addEventListener('DOMContentLoaded', async function () {
        await getClassList();
    }
);

async function getClassList() {
    try {
        const param = "";
        const response = await fetch('http://10.49.128.174:5000/api/classes?classList='+ encodeURIComponent(param));
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Fehler beim Laden:", error);
    }
}


