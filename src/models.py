from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    password = Column(String(255))

    bills = relationship("UserBillModel", back_populates="owner", cascade="all, delete-orphan")
    transactions = relationship("TransactionModel", back_populates="user", cascade="all, delete-orphan")
    record = relationship("RecordModel", back_populates="user", cascade="all, delete-orphan")




class UserBillModel(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(100), ForeignKey("users.name"))
    amount_of_money = Column(Integer, default=0.0)

    owner = relationship("UserModel", back_populates="bills")


class TransactionModel(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, ForeignKey('users.name'))
    amount = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserModel", back_populates="transactions")


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    record = relationship("RecordModel", back_populates="category", cascade="all, delete-orphan")



class RecordModel(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    date = Column(DateTime)
    amount = Column(Float)

    user = relationship("UserModel", back_populates="record")
    category = relationship("CategoryModel", back_populates="record")

