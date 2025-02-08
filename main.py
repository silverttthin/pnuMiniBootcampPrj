from fastapi import FastAPI

from controllers import UserController
from db import create_db

app = FastAPI()
create_db()

app.include_router(UserController.router)
