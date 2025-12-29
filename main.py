from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from mongodb.cliente import get_database
from routers import users, task, auth
from fastapi import FastAPI



app = FastAPI(
    title="TodoList API",
    description="API para gestionar tareas con autenticación JWT y MongoDB Atlas",
    version="1.0.0",
    contact={
        "name": "Wilson",
        "email": "wmjosemarquez@gmail.com",
        "url": "https://github.com/tu_usuario"
    }
)

# Conexión de routers
app.include_router(users.router, tags=["Usuarios"])
app.include_router(task.router, tags=["Tareas"])
app.include_router(auth.router, tags=["Autenticación"])

@app.get("/")
async def index():
    return {"Status": "To Do List is running"}

@app.get("/url")
async def url():
    return {"message": "Hola, FastAPI está funcionando!"}



#{
 # "username": "wilsondev",
  #"full_name": "Wilson Márquez",
  #"email": "wilson@example.com",
  #"password": "MiClaveSegura123",
  #"disabled": false
#}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

