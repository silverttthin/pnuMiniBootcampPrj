from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from etcs.enums import TripStyle
from models.Day import Day


class Plan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    writer_id: int = Field(foreign_key="user.id")
    local_name: str
    start_date: datetime
    end_date: datetime
    trip_style: TripStyle

    days: List["Day"] = Relationship()

