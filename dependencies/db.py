from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
from models import *

db_url = "sqlite:///TemuTriple.db"
db_engine = create_engine(db_url, connect_args={"check_same_thread": False})


def get_db_session():
    with Session(db_engine) as session:
        yield session


def create_db():
    SQLModel.metadata.create_all(db_engine)
