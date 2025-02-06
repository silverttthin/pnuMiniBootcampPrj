from fastapi import FastAPI
from db import create_db

app = FastAPI()
create_db()
