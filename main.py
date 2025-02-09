from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request
from pathlib import Path

import controllers
from routers import ChatbotHandlers
from controllers import UserController
from db import create_db

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        'home.html', {"request": request})

app.include_router(ChatbotHandlers.router)

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(controllers.PlanController.router)
app.include_router(UserController.router)

