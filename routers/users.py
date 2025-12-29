from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId 
from models.usersmodels import UserDB, UserUpdate, UserOut
from mongodb.cliente import get_user_collection
from security.auth import current_user, crypt

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"message":"Not found"}})

# 📌 Obtener todos los usuarios
@router.get("/", response_model=List[UserOut])
async def get_all_users():
    """logic to get all user as admin"""
    collection = await get_user_collection()
    user_cursor = collection.find()
    users = await user_cursor.to_list(length=100)

    return [
        UserOut(
            id=str(user["_id"]),
            username=user.get("username"),
            full_name=user.get("full_name"),
            email=user.get("email"),
            disabled=user.get("disabled"),
            role=user.get("role", "user")
        )
        for user in users
    ]
# 📌 Obtener usuario autenticado
@router.get("/me", response_model=UserOut)
async def get_me(user: UserOut = Depends(current_user)):
    """return the current user authenticated"""
    return user

#Signing up a new user
@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDB):
    collection = await get_user_collection()
    existing = await collection.find_one({"$or": [ 
        {"username": user.username}, 
        {"email": user.email}
    ]})
    if existing: 
        raise HTTPException(status_code=400, detail="Username or email already exists")
    hashed_password = crypt.hash(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password
    user_dict["role"] = "user"
    result = await collection.insert_one(user_dict) 
    created = await collection.find_one({"_id": result.inserted_id})
    if not created:
        raise HTTPException(status_code=500, detail="User creation failed")

    return UserOut( id=str(created["_id"]), 
                   username=created["username"],
                     full_name=created["full_name"], 
                     email=created["email"], 
                     disabled=created.get("disabled", False), 
                     role=created.get("role", "user") )

# 📌 Crear usuario
#@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
#async def create_user(user: UserDB):
#    """logic to create a new user"""
#    collection = await get_user_collection()
#    existing = await collection.find_one({"username": user.username})
#    if existing:
#        raise HTTPException(status_code=400, detail="Username already exists")
#    
#    hashed_password = crypt.hash(user.password)
    #    user_dict = user.model_dump()
#    user_dict["password"] = hashed_password
#    result = await collection.insert_one(user_dict)
#    created = await collection.find_one({"_id": result.inserted_id})
#    return UserOut(
#        id=str(created["_id"]),
#        username=created.get("username"),
#        full_name=created.get("full_name"),
#        email=created.get("email"),
#        disabled=created.get("disabled", False)
#    )


# 📌 UPDATING USER
@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: str,
    user_update: UserUpdate, 
    current: UserOut = Depends(current_user)
    ):
    """logic to update a user by id"""
    collection = await get_user_collection()

    # Validating the user can only update their own info
    if str(current.id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para modificar este usuario"
        )
    update_data = user_update.model_dump(exclude_unset=True)

    #validating rol change, only admin can change roles
    if "role" in update_data:
        if current.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only admin users can change roles"
            )

    # Encrypt password if it's being updated
    if "password" in update_data and update_data["password"]:
        update_data["password"] = crypt.hash(update_data["password"])

    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado o sin cambios"
        )

    updated_user = await collection.find_one({"_id": ObjectId(user_id)})
    if not updated_user:
        raise HTTPException(status_code=404, detail="user not found")

    return UserOut(
        id=str(updated_user["_id"]),
        username=updated_user.get("username"),
        full_name=updated_user.get("full_name"),
        email=updated_user.get("email"),
        disabled=updated_user.get("disabled"),
        role=updated_user.get("role", "user")
    )

# 📌 Eliminar usuario
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, _: UserOut = Depends(current_user)):
    """delete user by id"""
    collection = await get_user_collection()
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None