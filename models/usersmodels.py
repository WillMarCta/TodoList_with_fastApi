from typing import Optional, Annotated, Literal
from pydantic import BaseModel, EmailStr, constr

class User(BaseModel):
    """model for user without password"""
    username: str
    full_name: str
    email: EmailStr
    disabled: Optional[bool] = False
    role: Literal["user", "admin"] = "user"


class UserDB(User):
    """model for user with password"""
    password: Annotated[str, constr(min_length=8, max_length=72)]

class UserUpdate(BaseModel):
    """model for updating user information"""
    full_name: Optional[str]
    email: Optional[EmailStr]
    disabled: Optional[bool]
    password: Optional[Annotated[str, constr(min_length=8, max_length=72)]]
    role: Optional[Literal["user", "admin"]]

class UserOut(User):
    """model for user output without password"""
    id: str
