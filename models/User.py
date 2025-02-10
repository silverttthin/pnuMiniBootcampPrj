from dataclasses import dataclass
from typing import Optional, List, Union

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from models.Plan import Plan


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login_id: str = Field(index=True, unique=True)
    password: str = Field(exclude=True)
    name: Union[str, None] = None
    access_token: str | None = None
    created_at: int | None = Field(index=True)

    plans: List["Plan"] = Relationship()
