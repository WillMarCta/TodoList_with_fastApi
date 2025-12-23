const API_BASE = "http://127.0.0.1:8000";
const list = document.getElementById("list");
const createBtn = document.getElementById("create");

// ✅ Cargar tareas con numeración
async function cargarTareas() {
    const token = localStorage.getItem("accessToken");
    if (!token) {
        alert("⚠️ No estás autenticado. Inicia sesión primero.");
        window.location.href = "index.html";
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/tasks/`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const data = await res.json();

        if (res.ok) {
            list.innerHTML = "";
            data.forEach((task, index) => {
                const li = document.createElement("li");
                li.textContent = `${index + 1}. ${task.title} - ${task.description}`;

                // Botón editar
                const editBtn = document.createElement("button");
                editBtn.textContent = "✏️";
                editBtn.style.marginLeft = "10px";
                editBtn.onclick = () => editarTarea(task.id, task.title, task.description);

                // Botón eliminar
                const delBtn = document.createElement("button");
                delBtn.textContent = "🗑️";
                delBtn.style.marginLeft = "10px";
                delBtn.onclick = () => eliminarTarea(task.id);

                li.appendChild(editBtn);
                li.appendChild(delBtn);
                list.appendChild(li);
            });
        } else {
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("❌ Error cargando tareas");
        console.error(err);
    }
}

// ✅ Crear nueva tarea
createBtn.addEventListener("click", async () => {
    const token = localStorage.getItem("accessToken");
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    if (!title || !description) {
        alert("⚠️ Completa título y descripción");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/tasks/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ title, description })
        });

        if (res.ok) {
            alert("✅ Tarea creada");
            cargarTareas();
        } else {
            const data = await res.json();
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("❌ Error creando tarea");
        console.error(err);
    }
});

// ✅ Editar tarea
async function editarTarea(id, oldTitle, oldDescription) {
    const token = localStorage.getItem("accessToken");

    const nuevoTitulo = prompt("Nuevo título:", oldTitle);
    const nuevaDescripcion = prompt("Nueva descripción:", oldDescription);

    if (!nuevoTitulo || !nuevaDescripcion) {
        alert("⚠️ No se puede dejar vacío");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/tasks/${id}`, {
            method: "PUT", // también puedes usar PATCH si tu backend lo soporta
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ title: nuevoTitulo, description: nuevaDescripcion })
        });

        if (res.ok) {
            alert("✏️ Tarea actualizada");
            cargarTareas();
        } else {
            const data = await res.json();
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("❌ Error editando tarea");
        console.error(err);
    }
}

// ✅ Eliminar tarea
async function eliminarTarea(id) {
    const token = localStorage.getItem("accessToken");

    if (!confirm("¿Seguro que quieres eliminar esta tarea?")) return;

    try {
        const res = await fetch(`${API_BASE}/tasks/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (res.ok) {
            alert("🗑️ Tarea eliminada");
            cargarTareas();
        } else {
            const data = await res.json();
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("❌ Error eliminando tarea");
        console.error(err);
    }
}

// ✅ Botón salir
document.getElementById("logout").addEventListener("click", () => {
    localStorage.removeItem("accessToken");
    window.location.href = "index.html";
});


// 🚀 Inicializar
cargarTareas();
