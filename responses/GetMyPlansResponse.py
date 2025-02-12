from datetime import datetime
from typing import List

from pydantic import BaseModel


class PlaceResponse(BaseModel):
    place_name: str
    place_visit_time: datetime


class DayResponse(BaseModel):
    day_number: int
    places: List[PlaceResponse]


class PlanResponse(BaseModel):
    id: int
    writer_id: int
    local_name: str
    start_date: datetime
    end_date: datetime
    trip_style: str
    days: List[DayResponse]
