from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, constr

class User(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    disabled: Optional[bool] = False

class UserDB(User):
    password: Annotated[str, constr(min_length=8, max_length=72)]

class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    disabled: Optional[bool]
    password: Optional[Annotated[str, constr(min_length=8, max_length=72)]]

class UserOut(User):
    id: str
