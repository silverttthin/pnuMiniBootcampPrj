from dataclasses import dataclass
from typing import Optional, List, Union

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from models.Plan import Plan


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login_id: str = Field(index=True, unique=True)
    password: str
    name: Union[str,None] = None

    plans: List["Plan"] = Relationship()


class SignupResp(BaseModel):
    err_msg:str|None=None
    http_code:int|None=None


class SigninResp(BaseModel):
    jwt_token:str|None=None
    err_msg:str|None=None
    http_code:int|None=None

