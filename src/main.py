from fastapi import FastAPI
import uvicorn
from routers.healthcheck import router as router_healthcheck

app = FastAPI()

app.include_router(router_healthcheck)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
