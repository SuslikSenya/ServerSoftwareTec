# from fastapi import FastAPI, Request
# import uvicorn
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from starlette.middleware.cors import CORSMiddleware
#
# from backend.src.endpoints import user_router, db_router, record_router, category_router
# # from test import user_router, db_router, record_router, category_router
#
# app = FastAPI(
#     title="My FastAPI CRUD",
#     description="API для управления пользователями, категориями и записями",
#     version="1.0.0",
#     debug=True,
# )
#
# origins = [
#     "http://localhost:8000",
#     "http://127.0.0.1:5500",
# ]
#
# # templates = Jinja2Templates(directory="templates")
# # @app.get("/", response_class=HTMLResponse)
# # async def read_root(request: Request):
# #     return templates.TemplateResponse("index.html", {"request": request})
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# app.include_router(user_router)
# app.include_router(db_router)
# app.include_router(category_router)
# app.include_router(record_router)
#
# if __name__ == '__main__':
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)








from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import os

from backend.src.endpoints import user_router, db_router, record_router, category_router

app = FastAPI(
    title="My FastAPI CRUD",
    description="API для управления пользователями, категориями и записями",
    version="1.0.0",
    debug=True,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Обслуживание статических файлов (HTML, CSS, JS)
# app.mount("/static", StaticFiles(directory="frontend2"), name="static")


# @app.get("/", response_class=HTMLResponse)
# async def get_index():
#     with open("frontend_test/index.html", "r", encoding="utf-8") as file:
#         return file.read()


# Ваши роутеры
app.include_router(user_router)
app.include_router(db_router)
app.include_router(category_router)
app.include_router(record_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

