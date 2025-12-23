const API_BASE = "http://127.0.0.1:8000";

document.getElementById("login").addEventListener("click", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const body = new URLSearchParams();
        body.append("username", username);
        body.append("password", password);

        const res = await fetch(`${API_BASE}/auth/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("accessToken", data.access_token);
            alert("Login exitoso ✅");
            // Redirigir a tareas
            window.location.href = "tareas.html";
        } else {
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("❌ Error de conexión con el servidor");
        console.error(err);
    }
});
