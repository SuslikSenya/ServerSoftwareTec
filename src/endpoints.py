import json
from typing import List, Dict, Union

from fastapi import FastAPI, HTTPException, APIRouter

from models import User, Category, Record, UserCreate, CategoryCreate, CreateRecord

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


@user_router.delete("/{user_id}", response_model=Dict[str, str])
def delete_user(user_id: int) -> Dict[str, str]:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": f"User {user.name} deleted successfully!"}
    raise HTTPException(status_code=404, detail="User not found")


@user_router.post("", response_model=Dict[str, Union[str, User]], status_code=201)
def create_user(user: UserCreate) -> Dict[str, Union[str, User]]:
    id = len(users) + 1
    new_user = User(name=user.name, id=id)
    users.append(new_user)
    print(new_user)
    print(users)
    return {"message": f"User {new_user.name} created successful!", "User": new_user}


@user_router.get("/all_users/", response_model=List[User])
def get_all_users():
    return users


'''

##   CATEGORY 

'''


@category_router.get("/{category_id}", status_code=200)
def get_category(category_id: int) -> str:
    for category in categories:
        if category.id == category_id:
            return category.name
    raise HTTPException(status_code=404, detail="Category not found")


@category_router.delete("/{category_id}", response_model=Dict[str, str], status_code=201)
def delete_user(category_id: int) -> Dict[str, str]:
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return {"message": f"Category {category.name} deleted succesfully!"}
    raise HTTPException(status_code=404, detail="Category not found")


# Створення категорії витрат
@category_router.post("", response_model=Dict[str, Union[str, User]])
def create_category(category: CategoryCreate) -> Dict[str, Union[str, User]]:
    id = len(categories) + 1
    new_category = Category(name=category.name, id=id)
    categories.append(new_category)
    return {"message": "Category created successfully", "Category": new_category}


'''

##   RECORD  

'''


@record_router.get("/{record_id}", response_model=Record)
def get_record(record_id: int) -> Record:
    for record in records:
        if record.id == record_id:
            return record
    raise HTTPException(status_code=404, detail="Record not found")


@record_router.delete("/{record_id}", response_model=Dict[str, str])
def delete_user(record_id: int) -> Dict[str, str]:
    for record in records:
        if record.id == record_id:
            records.remove(record)
            return {"message": f"Record deleted succesfully!"}
    raise HTTPException(status_code=404, detail="Record not found")


@record_router.post("", response_model=Dict[str, Record])
def create_record(record: CreateRecord) -> Dict[str, Record]:
    id = len(records) + 1
    new_record = Record(
        user_id=record.user_id,
        category_id=record.category_id,
        date=record.date,
        amount=record.amount,
        id=id)
    records.append(new_record)
    return {"Record": new_record}


@record_router.get("")
def get_categories(user_id: int = None, category_id: int = None):
    if user_id is None and category_id is None:
        raise HTTPException(status_code=404, detail="Expected at list one parameter")

    filtered_records: List[Record] = []

    for record in records:
        if record.user_id == user_id and category_id is None:
            filtered_records.append(record)
        elif record.category_id == category_id and user_id is None:
            filtered_records.append(record)
        elif (user_id is not None and record.user_id == user_id) and (
                category_id is not None and record.category_id == category_id):
            filtered_records.append(record)
    if filtered_records:
        return filtered_records
    raise HTTPException(status_code=404, detail="No records found")

