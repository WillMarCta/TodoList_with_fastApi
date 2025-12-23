import asyncio
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

async def get_client():
    uri = "mongodb+srv://wmarquez:25859068Ww..@willmar.ro1lrnr.mongodb.net/?appName=willmar"
    client = AsyncMongoClient(uri, server_api=ServerApi('1'))
    return client

#obteniendo la base de datos principal
async def get_database():
    client = await get_client()
    return client["main_db"]


async def get_task_collection():
    """#funcion para obtener la coleccion de tareas"""
    db = await get_database()
    return db.get_collection("tasks")


async def get_user_collection():
    """#funcion para obtener la coleccion de usuarios"""
    db = await get_database()
    return db.get_collection("users")

async def ping_server():
    """#funcion para verificar la conexion con el servidor"""
    client = await get_client()
    try:
        await client.admin.command("ping")
        print("✅ Conectado a MongoDB Atlas")
    except Exception as e:
        print("❌ Error:", e)
        
if __name__ == "__main__":
    asyncio.run(ping_server())# 📌 Propósito: Configuración de la conexión a MongoDB.