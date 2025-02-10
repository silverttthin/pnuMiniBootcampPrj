from typing import Annotated

from fastapi import APIRouter, Depends, Body, Request
from fastapi.responses import HTMLResponse

from dependencies.db import get_db_session
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from requests.plan_schema import PlanCreate, PlanDeleteRequest, GetMyPlanListRequest
from services.PlanService import PlanService

router = APIRouter(prefix="/plans", tags=["Plan"])
templates = Jinja2Templates(directory="templates")


# 세션을 주입받은 서비스 인스턴스 생성
def get_plan_service(db: Session = Depends(get_db_session)) -> PlanService:
    return PlanService(db)

# todo: 결과물을 CommonResponse에 담아야 함


# 계획 생성
@router.post("")
async def create_plan(req: Annotated[PlanCreate, Body(
    examples=[
        {
            "writer_id": 1,
            "local_name": "부산",
            "start_date": "2025-03-01T00:00:00",
            "end_date": "2025-03-03T00:00:00",
            "trip_style": "관광보다 먹방",  # TripStyle Enum 값
            "days": [
                {
                    "day_number": 1,
                    "places": [
                        {
                            "place_name": "톤쇼우 부산대점",
                            "place_visit_time": "2025-03-01T10:00:00"
                        },
                        {
                            "place_name": "수수굉 부산대점",
                            "place_visit_time": "2025-03-01T14:00:00"
                        }
                    ]
                },
                {
                    "day_number": 2,
                    "places": [
                        {
                            "place_name": "미가락",
                            "place_visit_time": "2025-03-02T11:00:00"
                        }
                    ]
                }
            ]
        }
    ])], planService: PlanService = Depends(get_plan_service)):
    created_plan_id = planService.create_plan(req)
    return {"plan_id": created_plan_id}


# 계획 삭제
@router.delete("")
async def delete_plan(req: PlanDeleteRequest, planService: PlanService = Depends(get_plan_service)):
    return planService.delete_plan(req)


# 내가 작성한 게획 리스트 가져오기
@router.post("/list")
async def get_my_plans(req: GetMyPlanListRequest,
                       planService: PlanService = Depends(get_plan_service)):
    plans = planService.get_my_plans(req)
    return plans


# 플랜 작성 및 목록 페이지 라우팅
@router.get("/page", response_class=HTMLResponse)
async def read_plan_page(request: Request, planService: PlanService = Depends(get_plan_service)):
    # todo: JWT token 받아 decoding 하기
    user_id: int = 1
    user_name: str = "이시웅"
    plans = planService.get_my_plans(
        GetMyPlanListRequest(user_id=user_id)
    )

    return templates.TemplateResponse(
        request=request, name="plan.html", context={
            "plans": plans,
            "user": {
                "user_id": user_id,
                "user_name": user_name,
            }
        }
    )