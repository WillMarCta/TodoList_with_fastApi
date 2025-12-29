 # get_current_user, dependencias
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from models.usersmodels import UserOut, UserDB
from mongodb.cliente import get_user_collection
from security.jwt_handler import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def search_user(username: str) -> UserDB | None:
    """Function to search for a user by username including password"""
    collection = await get_user_collection()
    user_data = await collection.find_one({"username": username})
    if user_data:
        return UserDB(**user_data)
    return None

async def search_user_public(username: str) -> UserOut | None:
    """#function to search for a user without returning the password"""
    collection = await get_user_collection()
    user_data = await collection.find_one({"username": username})
    if user_data:
        user_data.pop("password", None)
        return UserOut(
            id=str(user_data["_id"]),
            username=user_data["username"],
            full_name=user_data["full_name"],
            email=user_data["email"],
            disabled=user_data.get("disabled", False),
            role=user_data.get("role", "user")
        )
    return None


async def auth_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    """#function to get the current authenticated user"""
    try:
        username = decode_access_token(token)
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

async def current_user(user: UserOut = Depends(auth_user)) -> UserOut:
    """#function to get the current active user"""
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user")
    return user

async def admin_required(user: UserOut = Depends(current_user)):
    """Function to check if the current user has admin role"""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="admin privileges required"
        )
    return user