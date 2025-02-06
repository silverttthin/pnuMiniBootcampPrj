from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    day_id: int = Field(foreign_key="day.id")
    place_name: str
    place_visit_time: datetime



