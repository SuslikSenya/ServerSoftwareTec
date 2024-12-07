from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str


class User(UserCreate):
    id: int


class UserBillCreate(BaseModel):
    user_name: str
    amount_of_money: int


class UserBill(UserBillCreate):
    id: int


class TransactionCreate(BaseModel):
    user_name: str
    amount: int
    description: str
    timestamp: datetime

class Transaction(TransactionCreate):
    id: int


class CategoryCreate(BaseModel):
    name: str


class Category(CategoryCreate):
    id: int


class CreateRecord(BaseModel):
    user_id: int
    category_id: int
    date: datetime = datetime.now()
    amount: float


class Record(CreateRecord):
    id: int