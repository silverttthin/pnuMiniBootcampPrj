from fastapi import APIRouter, Depends

from db import get_db_session
from sqlalchemy.orm import Session
from requests.plan_schema import PlanCreate
from services import PlanService

router = APIRouter(prefix="/plans", tags=["Plan"])


@router.post("")
async def create_plan(req: PlanCreate, session: Session = Depends(get_db_session)):
    """
    계획 생성 API
    요청 JSON 예시:
    {
        "writer_id": 1,
        "local_name": "부산",
        "start_date": "2025-03-01T00:00:00",
        "end_date": "2025-03-05T00:00:00",
        "trip_style": "FOOD",   # TripStyle Enum 값
        "days": [
            {
                "day_number": 1,
                "places": [
                    {
                        "place_name": "경복궁",
                        "place_visit_time": "2025-03-01T10:00:00"
                    },
                    {
                        "place_name": "인사동",
                        "place_visit_time": "2025-03-01T14:00:00"
                    }
                ]
            },
            {
                "day_number": 2,
                "places": [
                    {
                        "place_name": "남산타워",
                        "place_visit_time": "2025-03-02T11:00:00"
                    }
                ]
            }
        ]
    }
    """
    # todo: 결과물을 CommonResponse에 담아야 함
    created_plan_id =  PlanService.create_plan(req, session)
    return {"plan_id": created_plan_id}

