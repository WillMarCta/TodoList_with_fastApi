const API_BASE = "http://127.0.0.1:8000";

document.getElementById("signupForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // El backend espera también `full_name` según el modelo UserDB. Usamos username como full_name si no hay un campo separado.
    const full_name = username;

    try {
        const res = await fetch(`${API_BASE}/users/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, full_name, email, password })
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok) {
            const status = document.getElementById("signupStatus");
            status.textContent = "✅ Registro exitoso. Redirigiendo...";
            status.style.color = "green";

            setTimeout(() => {
                window.location.href = "index.html";
            }, 2000);
            return;
        }

        // Manejar errores devueltos por Pydantic/FastAPI (puede ser una lista de objetos)
        let message = "Error desconocido";
        if (data) {
            if (typeof data.detail === 'string') {
                message = data.detail;
            } else if (Array.isArray(data.detail)) {
                message = data.detail.map(d => d.msg || d.message || JSON.stringify(d)).join(', ');
            } else if (data.message) {
                message = data.message;
            } else {
                message = JSON.stringify(data);
            }
        }

        const statusEl = document.getElementById("signupStatus");
        statusEl.textContent = `❌ Error: ${message}`;
        statusEl.style.color = "red";
    } catch (err) {
        const statusEl = document.getElementById("signupStatus");
        statusEl.textContent = "❌ Error de conexión con el servidor";
        statusEl.style.color = "red";
        console.error(err);
    }
});
