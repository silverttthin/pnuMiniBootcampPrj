from datetime import datetime
from typing import List

from pydantic import BaseModel
from etcs.enums import TripStyle


class PlaceCreate(BaseModel):
    place_name: str
    place_visit_time: datetime


class DayCreate(BaseModel):
    day_number: int
    places: List[PlaceCreate]


class PlanCreate(BaseModel):
    writer_id: int
    local_name: str
    start_date: datetime
    end_date: datetime
    trip_style: TripStyle
    days: List[DayCreate]


class PlanDeleteRequest(BaseModel):
    plan_id: int
    user_id: int
