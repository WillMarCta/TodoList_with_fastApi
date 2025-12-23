# solo endpoints de login/registro
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.usersmodels import User
from security.auth import search_user, crypt, current_user
from security.jwt_handler import create_acess_token


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """#endpoint para el login de usuarios"""
    user = await search_user(form.username)
    if not user or not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_acess_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def me(user: User = Depends(current_user)):
    """#endpoint para obtener el usuario actual autenticado"""
    return user