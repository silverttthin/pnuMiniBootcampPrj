from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request
from pathlib import Path

from routers import ChatbotHandlers, PlanController
from routers import UserController
from dependencies.db import create_db

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

app.include_router(PlanController.router)
app.include_router(UserController.router)

