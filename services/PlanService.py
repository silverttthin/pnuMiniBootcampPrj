from fastapi import HTTPException
from models import User, Plan, Day, Place
from requests.plan_schema import PlanCreate
from sqlalchemy.orm import Session


# 계획 생성 API
def create_plan(plan_data: PlanCreate, session: Session):
    # 유저 검증
    user = session.get(User, plan_data.writer_id)
    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다.")

    # Plan 생성
    plan = Plan(
        writer_id=plan_data.writer_id,
        local_name=plan_data.local_name,
        start_date=plan_data.start_date,
        end_date=plan_data.end_date,
        trip_style=plan_data.trip_style,
    )
    session.add(plan)
    session.commit()
    session.refresh(plan)  # 요청 days에 fk로 넣기위해 PK 가져오는 용도

    # 각 Day 생성
    for day_data in plan_data.days:
        day = Day(
            plan_id=plan.id,
            day_number=day_data.day_number,
        )
        session.add(day)
        session.commit()
        session.refresh(day) # 요청 places에 fk로 넣기위해 PK 가져오는 용도

        # 하나의 Day마다 여러개 들어가는 Place 정보 매핑
        for place_data in day_data.places:
            place = Place(
                day_id=day.id,
                place_name=place_data.place_name,
                place_visit_time=place_data.place_visit_time,
            )
            session.add(place)

        # 한 일정에 들어가는 장소들 add한것 전부 커밋
        session.commit()

    session.refresh(plan)

    return plan.id


def delete_plan(plan_id, user_id, session):
    # 1. 계획 가져오기
    plan = session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="삭제하고자 하는 계획이 존재하지 않습니다.")

    # 2. 요청자가 해당 플랜 게시자인지 검증
    if plan.writer_id != user_id:
        raise HTTPException(status_code=403, detail="게시자만이 계획을 삭제할 수 있습니다.")

    # 3. 플랜의 각 일자를 순회해 장소들을 삭제하고 일자 삭제
    days = plan.days
    for day in days:
        places = day.places
        for place in places:
            session.delete(place)
        session.delete(day)

    # 4. 플랜 삭제 후 세션 커밋
    session.delete(plan)
    session.commit()
    return {"result": 'ok'}
