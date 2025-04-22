import re
from typing import Dict
from fastapi.responses import JSONResponse

from fastapi import FastAPI, Request

from fastapi import FastAPI, HTTPException, APIRouter, Depends, status, Security, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware

from .database import get_async_session, Base, engine
from .schemas import Token, User, UserBill, UserCreate, TransactionCreate, Transaction, CategoryCreate, CreateRecord, \
    LoginUser
from .models import UserModel, UserBillModel, TransactionModel, CategoryModel, RecordModel

from datetime import timedelta, datetime

from .utils import authenticate_user, create_access_token, verify_password, get_password_hash, get_current_user, \
    ACCESS_TOKEN_EXPIRE_MINUTES, get_user

from async_lru import alru_cache

user_router = APIRouter(tags=['Users'], prefix='/user')
db_router = APIRouter(tags=['DB START'], prefix='/admin')
category_router = APIRouter(tags=['Categories'], prefix='/category')
record_router = APIRouter(tags=['Records'], prefix='/record')

'''

##   ADMIN

'''


@db_router.post("/setup/")
async def setup_database():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        return {"message": "Database setup successful."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database setup failed")


@alru_cache()
async def fetch_all_users():
    async for session in get_async_session():  # Открываем сессию внутри
        result = await session.execute(select(UserModel))
        return result.scalars().all()


@db_router.get("/all_users/")
async def get_all_users():
    all_users = await fetch_all_users()
    if not all_users:
        raise HTTPException(status_code=404, detail="Users not found")
    return all_users


'''

##   USER 

'''


@user_router.post("/login")
async def login_user(
        username: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_async_session)
):
    login_user = await authenticate_user(user_name=username, password=password, session=session)

    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": login_user.name}, expires_delta=access_token_expire)
    return {"access_token": access_token, "token_type": "bearer", "user": login_user.name}


@user_router.post("/register/", status_code=status.HTTP_201_CREATED)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if not re.match(r'^[A-Za-z0-9]+$', user.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username can only contain alphanumeric characters.")

        hashed_password = get_password_hash(user.password)

        async with session.begin():
            new_user = UserModel(name=user.name, password=hashed_password)
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
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    query = select(UserModel).filter(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    query_bill = select(UserBillModel).filter(UserBillModel.user_name == user.name)
    result_bill = await session.execute(query_bill)
    user_bill = result_bill.scalars().first()

    return {"id": user.id, "name": user.name, "user_bill": user_bill.amount_of_money}


@user_router.get("/get_user_by_name/{user_name}")
async def get_user_by_name(
        user_name: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    user = await get_user(user_name=user_name, session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    query_bill = select(UserBillModel).filter(UserBillModel.user_name == user.name)
    result_bill = await session.execute(query_bill)
    user_bill = result_bill.scalars().first()

    return {"id": user.id, "name": user.name, "user_bill": user_bill.amount_of_money}


@user_router.delete("/{user_id}")
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
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


@user_router.post("/create_transaction/", status_code=200)
async def create_transaction(
        transaction: TransactionCreate,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    try:
        naive_timestamp = transaction.timestamp.replace(tzinfo=None)
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
                timestamp=naive_timestamp,
                description=transaction.description
            )
            session.add(new_transaction)
            await session.commit()

        return transaction
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


'''

##   CATEGORY

'''

# # immediately after imports
# class RateLimitingMiddleware(BaseHTTPMiddleware):
#     # Rate limiting configurations
#     RATE_LIMIT_DURATION = timedelta(minutes=1)
#     RATE_LIMIT_REQUESTS = 3
#
#     def __init__(self, app):
#         super().__init__(app)
#         # Dictionary to store request counts for each IP
#         self.request_counts = {}
#
#     async def dispatch(self, request, call_next):
#         # Get the client's IP address
#         client_ip = request.client.host
#
#         # Check if IP is already present in request_counts
#         request_count, last_request = self.request_counts.get(client_ip, (0, datetime.min))
#
#         # Calculate the time elapsed since the last request
#         elapsed_time = datetime.now() - last_request
#
#         if elapsed_time > self.RATE_LIMIT_DURATION:
#             # If the elapsed time is greater than the rate limit duration, reset the count
#             request_count = 1
#         else:
#             if request_count >= self.RATE_LIMIT_REQUESTS:
#                 # If the request count exceeds the rate limit, return a JSON response with an error message
#                 return JSONResponse(
#                     status_code=429,
#                     content={"message": "Rate limit exceeded. Please try again later."}
#                 )
#             request_count += 1
#
#         # Update the request count and last request timestamp for the IP
#         self.request_counts[client_ip] = (request_count, datetime.now())
#
#         # Proceed with the request
#         response = await call_next(request)
#         return response
#
#
#
# category_router.add_middleware(RateLimitingMiddleware)



@category_router.get("/{category_id}", status_code=200)
async def get_category(
        category_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
) -> str:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized")

    query = select(CategoryModel).filter(CategoryModel.id == category_id)
    result = await session.execute(query)
    category = result.scalars().first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.name


@category_router.delete("/{category_id}", status_code=201)
async def delete_category(
        category_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
) -> Dict[str, str]:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized")
    query = select(CategoryModel).filter(CategoryModel.id == category_id)
    result = await session.execute(query)
    category = result.scalars().first()
    if category:
        await session.delete(category)
        await session.commit()
        return {"message": f"Category {category.name} deleted successfully!"}
    raise HTTPException(status_code=404, detail="Category not found")


@category_router.post("")
async def create_category(
        category: CategoryCreate,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized")
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
async def get_record(
        record_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized")
    query = select(RecordModel).filter(RecordModel.id == record_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@record_router.delete("/{record_id}")
async def delete_record(
        record_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized")
    query = select(RecordModel).filter(RecordModel.id == record_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        await session.delete(record)
        await session.commit()
        return {"message": "Record deleted successfully!"}
    raise HTTPException(status_code=404, detail="Record not found")


@record_router.post("")
async def create_record(
        record: CreateRecord,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized")
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
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to create record")


@record_router.get("")
async def get_records(
        # user_id: int = None,
        category_id: int = None,
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized")

    user_id = current_user.id
    if user_id is None and category_id is None:
        raise HTTPException(status_code=400, detail="Expected at least one parameter")

    query = select(RecordModel)
    if user_id is not None:
        query = query.filter(RecordModel.user_id == user_id)
    if category_id is not None:
        query = query.filter(RecordModel.category_id == category_id)

    result = await session.execute(query)
    filtered_records = result.scalars().all()

    # if not filtered_records:
    #     return JSONResponse(
    #         status_code=404,
    #         content={
    #             "data": None,
    #             "error": {
    #                 "status_code": 404,
    #                 "detail": "No records found"
    #             }
    #         }
    #     )

    return {
            "data": filtered_records,
            "status_code": 200
        }
