from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from pathlib import Path
from routers import (HomeController, ChatbotController, PlanController, UserController, HomeController)
from dependencies.db import create_db

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static"
)

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(HomeController.router)
app.include_router(ChatbotController.router)
app.include_router(PlanController.router)
app.include_router(UserController.router)

