import uvicorn
from fastapi import FastAPI

from app.routers import routers

app = FastAPI()

_ = [app.include_router(router) for router in routers]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
