import json
from typing import List, Dict, Union

from fastapi import FastAPI, HTTPException, APIRouter

from src.models import User, Category, Record, UserCreate

user_router = APIRouter(tags=['Users'], prefix='/user')
category_router = APIRouter(tags=['Categories'], prefix='/category')
record_router = APIRouter(tags=['Records'], prefix='/record')

users: List[User] = []
categories: List[Category] = []
records: List[Record] = []

'''

##   USER 

'''


@user_router.get("/{user_id}")
def get_user(user_id: int) -> str:
    for user in users:
        if user.id == user_id:
            return user.name
    raise HTTPException(status_code=404, detail="User not found")


@user_router.delete("/{user_id}")
def delete_user(user_id: int) -> Dict[str, str]:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": f"User {user.name} deleted successfully!"}
    raise HTTPException(status_code=404, detail="User not found")


@user_router.post("/")
def create_user(user: UserCreate):
    id = len(users) + 1
    new_user = User(name=user.name, id=id)
    users.append(new_user)
    print(new_user)
    print(users)
    return {"message": "User created successfully", "user": new_user.name}


@user_router.get("/all_users/", response_model=List[User])
def get_all_users():
    return users