from typing import Optional
from pydantic import BaseModel



class TodoItem(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None
    done: Optional[bool] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
    user_id: Optional[int] = None