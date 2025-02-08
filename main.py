from fastapi import FastAPI
import controllers
from controllers import UserController
from db import create_db

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db()


app.include_router(controllers.PlanController.router)
app.include_router(UserController.router)

