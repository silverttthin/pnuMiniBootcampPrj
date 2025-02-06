from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from models.Plan import Plan


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login_id: str = Field(index=True, unique=True)
    password: str
    name: str

    plans: List["Plan"] = Relationship()
