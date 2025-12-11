import { getTeacherDetailedData } from './getTeacherDetailedData.js';

document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById("detailBody");
    if (!tbody) {
        console.error("❌ #detailBody existiert nicht im DOM. Script nur auf Detailseite laden!");
        return;
    }

    const class_name = sessionStorage.getItem("class_name");
    const half_year = sessionStorage.getItem("half_year");

    if (!class_name || !half_year) {
        showAlert("❌ Fehlende Informationen – bitte erneut auswählen.");
        return;
    }

    getTeacherDetailedData(class_name, half_year);
});
