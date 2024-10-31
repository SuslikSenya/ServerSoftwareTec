from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str


class User(UserCreate):
    id: int = 0


class CategoryCreate(BaseModel):
    name: str


class Category(CategoryCreate):
    id: int = 0


class CreateRecord(BaseModel):
    user_id: int
    category_id: int
    date: datetime = datetime.now()
    amount: float


class Record(CreateRecord):
    id: int = 0
