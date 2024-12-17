from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    name: str
    password: bytes


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
