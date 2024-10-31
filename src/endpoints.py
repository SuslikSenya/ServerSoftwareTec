from fastapi import FastAPI, HTTPException
from models import User, Category, Record

app = FastAPI()

# Імітуємо базу даних з використанням списків
users = []
categories = []
expense_records = []

# Створення користувача
@app.post("/users/")
def create_user(user: User):
    users.append(user)
    return {"message": "User created successfully", "user": user}

# Створення категорії витрат
@app.post("/categories/")
def create_category(category: Category):
    categories.append(category)
    return {"message": "Category created successfully", "category": category}

# Створення запису про витрати
@app.post("/expenses/")
def create_expense_record(expense: Record):
    expense_records.append(expense)
    return {"message": "Expense record created successfully", "expense": expense}

# Отримання списку категорій
@app.get("/categories/", response_model=List[Category])
def get_categories():
    return categories

# Отримання списку записів по певному користувачу
@app.get("/expenses/user/{user_id}", response_model=List[Record])
def get_expenses_by_user(user_id: int):
    user_expenses = [record for record in expense_records if record.user_id == user_id]
    return user_expenses

# Отримання списку записів в категорії для певного користувача
@app.get("/expenses/user/{user_id}/category/{category_id}", response_model=List[Record])
def get_expenses_by_user_and_category(user_id: int, category_id: int):
    filtered_expenses = [
        record for record in expense_records
        if record.user_id == user_id and record.category_id == category_id
    ]
    return filtered_expenses