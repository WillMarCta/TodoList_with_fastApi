from bson import ObjectId #Convierte el string en un ObjectId
from fastapi import APIRouter, HTTPException
from models.taskmodels import TodoItem, TaskUpdate
from mongodb.cliente import get_task_collection


router = APIRouter(prefix="/tasks", tags=["task"], responses={404: {"message":"Not found"}})

#La idea es que cada endpoint de tu API tenga un response_model adecuado a lo que devuelve, 
# no tanto “por cada tarea” literal, sino por cada operación que expone tu API.

@router.get("/", response_model=list[TodoItem])
async def get_all_tasks():
    """logica para obtener todas las tareas"""
    collection = await get_task_collection()
    task_cursor = collection.find()
    tasks = await task_cursor.to_list(length=100)

    return [
        TodoItem(
            id=str(task["_id"]),
            name=task.get("name"),
            title=task.get("title"),
            description=task.get("description"),
            user_id=task.get("user_id"),
            done=task.get("done")

        )
        for task in tasks
    ]

@router.post("/")
async def post_task(task: TodoItem):
    """logic to create a new task"""
    collection =await get_task_collection()
    result = await collection.insert_one(task.model_dump())
    return {"message": "Task Created", "id": str(result.inserted_id)}

@router.put("/{task_id}")
async def update_task(task_id: str, task: TaskUpdate):
    """logic to be able to update a task"""
    collection = await get_task_collection()
    result = await collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task.model_dump(exclude_unset=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Task not found or no changes detected")
    return {"Message": "Task updated"}

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """logic to delete a task"""
    collection = await get_task_collection()
    result = await collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}