 # get_current_user, dependencias
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from models.usersmodels import User, UserDB
from mongodb.cliente import get_user_collection
from security.jwt_handler import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def search_user(username: str) -> UserDB | None:
    """#funcion para buscar un usuario en la base de datos"""
    collection = await get_user_collection()
    user_data = await collection.find_one({"username": username})
    if user_data:
        return UserDB(**user_data)
    return None

async def search_user_public(username: str) -> User | None:
    """#funcion para buscar un usuario sin devolver la contraseña"""
    collection = await get_user_collection()
    user_data = await collection.find_one({"username": username})
    if user_data:
        #eliminamos la contrasena antes de crear onjeto User
        user_data.pop("password", None)
        return User(**user_data)
    return None


async def auth_user(token: str = Depends(oauth2_scheme)) -> User:
    """#funcion para obtener el usuario actual autenticado"""
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    user = await search_user_public(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def current_user(user: User = Depends(auth_user)) -> User:
    """#funcion para obtener el usuario actual y verificar si esta activo"""
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user")
    
    return user