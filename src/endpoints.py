import json
import re
from typing import List, Dict, Union

from fastapi import FastAPI, HTTPException, APIRouter, Depends, status
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_async_session
from schemas import User, UserBill, UserCreate, TransactionCreate, Transaction, CategoryCreate, CreateRecord
from models import UserModel, UserBillModel, TransactionModel, CategoryModel, RecordModel

user_router = APIRouter(tags=['Users'], prefix='/user')
db_router = APIRouter(tags=['DB START'], prefix='/db')
category_router = APIRouter(tags=['Categories'], prefix='/category')
record_router = APIRouter(tags=['Records'], prefix='/record')



# @db_router.post("/setup")
# async def setup_database():
#     try:
#         async with engine.begin() as conn:
#             await conn.run_sync(Base.metadata.drop_all)
#             await conn.run_sync(Base.metadata.create_all)
#         return {"message": "Database setup successful."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Database setup failed")


'''

##   USER 

'''



@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        if not re.match(r'^[A-Za-z0-9]+$', user.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username can only contain alphanumeric characters.")

        async with session.begin():
            new_user = UserModel(name=user.name)
            session.add(new_user)
            await session.flush()

            new_bill = UserBillModel(user_name=new_user.name)
            session.add(new_bill)

        await session.commit()
        await session.refresh(new_user)
        await session.refresh(new_bill)

        return {"id": new_user.id, "name": new_user.name, "user_bill": new_bill.amount_of_money}

    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User name already exists")


@user_router.get("/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(UserModel).filter(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    query_bill = select(UserBillModel).filter(UserBillModel.user_name == user.name)
    result_bill = await session.execute(query_bill)
    user_bill = result_bill.scalars().first()
    return {"id": user.id, "name": user.name, "user_bill": user_bill.amount_of_money}


@user_router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(UserModel).filter(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user_name = user.name

    await session.delete(user)
    await session.commit()

    return {'detail': f"User '{user_name}' was deleted successfully!"}


@user_router.post("/create_transaction", status_code=200)
async def create_transaction(transaction: TransactionCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        async with session:
            query = select(UserBillModel).filter(UserBillModel.user_name == transaction.user_name)
            result = await session.execute(query)
            user_bill = result.scalars().first()
            if user_bill is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            user_bill.amount_of_money += transaction.amount
            new_transaction = TransactionModel(
                user_name=transaction.user_name,
                amount=transaction.amount,
                timestamp=transaction.timestamp,
                description=transaction.description
            )
            session.add(new_transaction)
            await session.commit()

        return transaction
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@user_router.get("/all_users/")
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(UserModel))
    all_users = result.scalars().all()
    print(all_users)
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")

    return all_users


'''

##   CATEGORY

'''


@category_router.get("/{category_id}", status_code=200)
async def get_category(category_id: int, session: AsyncSession = Depends(get_async_session)) -> str:
    query = select(CategoryModel).filter(CategoryModel.id == category_id)
    result = await session.execute(query)
    category = result.scalars().first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.name


@category_router.delete("/{category_id}", status_code=201)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_async_session)) -> Dict[str, str]:
    query = select(CategoryModel).filter(CategoryModel.id == category_id)
    result = await session.execute(query)
    category = result.scalars().first()
    if category:
        await session.delete(category)
        await session.commit()
        return {"message": f"Category {category.name} deleted successfully!"}
    raise HTTPException(status_code=404, detail="Category not found")


@category_router.post("")
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        if not category.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name cannot be empty.")
        new_category = CategoryModel(name=category.name)
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return {"message": "Category created successfully", "Category": new_category}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



'''

##   RECORD

'''


@record_router.get("/{record_id}")
async def get_record(record_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(RecordModel).filter(RecordModel.id == record_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@record_router.delete("/{record_id}")
async def delete_record(record_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(RecordModel).filter(RecordModel.id == record_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        await session.delete(record)
        await session.commit()
        return {"message": "Record deleted successfully!"}
    raise HTTPException(status_code=404, detail="Record not found")

@record_router.post("")
async def create_record(record: CreateRecord, session: AsyncSession = Depends(get_async_session)):
    try:
        new_record = RecordModel(
            user_id=record.user_id,
            category_id=record.category_id,
            date=record.date,
            amount=record.amount,
        )
        session.add(new_record)
        await session.commit()
        await session.refresh(new_record)
        return {"Record": new_record}
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"Validation error: {ve.errors()}")
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Integrity error: invalid user or category id")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create record")

@record_router.get("")
async def get_records(user_id: int = None, category_id: int = None, session: AsyncSession = Depends(get_async_session)):
    if user_id is None and category_id is None:
        raise HTTPException(status_code=400, detail="Expected at least one parameter")

    query = select(RecordModel)
    if user_id is not None:
        query = query.filter(RecordModel.user_id == user_id)
    if category_id is not None:
        query = query.filter(RecordModel.category_id == category_id)

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User and category not found")

    result = await session.execute(query)
    filtered_records = result.scalars().all()

    if filtered_records:
        return filtered_records
    raise HTTPException(status_code=404, detail="No records found")

