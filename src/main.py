from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.endpoints import user_router, record_router, category_router

app = FastAPI(debug=True)

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(user_router)
app.include_router(category_router)
app.include_router(record_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
