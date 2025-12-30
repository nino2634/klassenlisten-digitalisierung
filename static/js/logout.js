// Optional, falls es mal benötigt wird, aktuell wird man automatisch ausgeloggt, wenn man den Browser schließt
async function logout() {
    try {
        const response = await fetch("/logout", {
            method: "GET",   // deine Route ist GET
            credentials: "include" // wichtig, damit Cookies/Sessions mitgeschickt werden
        });

        if (response.ok) {
            // Logout erfolgreich → z. B. zur Login-Seite weiterleiten
            window.location.href = "/";
        } else {
            console.error("Logout fehlgeschlagen");
        }
    } catch (error) {
        console.error("Netzwerkfehler beim Logout:", error);
    }
}
