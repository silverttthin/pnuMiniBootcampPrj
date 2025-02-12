from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from models.Place import Place


class Day(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    day_number: int  # 여행 계획 내 몇 번째 날인지를 나타냄

    places: List["Place"] = Relationship()