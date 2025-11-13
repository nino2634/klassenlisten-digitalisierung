document.addEventListener('DOMContentLoaded', function() {
document.getElementById("login-button").addEventListener("click", getUserVerification);

})

async function getUserVerification() {
try {
    const user = document.getElementById('user').innerHTML
    const password = document.getElementById('pass').innerHTML
    const response = await fetch('http://10.49.128.174:5000/api/verify_user?user='
    + encodeURIComponent(userTMP)
    +'&password='+ encodeURIComponent(passwordTMP)); 
    const data = await response.text();
    console.log(data);
} catch (error) {
    console.error("Fehler beim Laden:", error);
}

}
