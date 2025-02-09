from typing import List

from fastapi import HTTPException
from models import User, Plan, Day, Place
from requests.plan_schema import PlanCreate
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from responses.GetMyPlansResponse import PlaceResponse, PlanResponse, DayResponse


class PlanService:
    def __init__(self, session: Session):
        self.session = session

    # 계획 생성 API
    def create_plan(self, plan_data: PlanCreate):
        # 유저 검증
        user = self.session.get(User, plan_data.writer_id)
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
        self.session.add(plan)
        self.session.commit()
        self.session.refresh(plan)  # 요청 days에 fk로 넣기위해 PK 가져오는 용도

        # 각 Day 생성
        for day_data in plan_data.days:
            day = Day(
                plan_id=plan.id,
                day_number=day_data.day_number,
            )
            self.session.add(day)
            self.session.commit()
            self.session.refresh(day)  # 요청 places에 fk로 넣기위해 PK 가져오는 용도

            # 하나의 Day마다 여러개 들어가는 Place 정보 매핑
            for place_data in day_data.places:
                place = Place(
                    day_id=day.id,
                    place_name=place_data.place_name,
                    place_visit_time=place_data.place_visit_time,
                )
                self.session.add(place)

            # 한 일정에 들어가는 장소들 add한것 전부 커밋
            self.session.commit()

        self.session.refresh(plan)

        return plan.id

    # 계획 삭제 API
    def delete_plan(self, req):
        # 1. 계획 가져오기
        plan = self.session.get(Plan, req.plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="삭제하고자 하는 계획이 존재하지 않습니다.")

        # 2. 요청자가 해당 플랜 게시자인지 검증
        if plan.writer_id != req.user_id:
            raise HTTPException(status_code=403, detail="게시자만이 계획을 삭제할 수 있습니다.")

        # 3. 플랜의 각 일자를 순회해 장소들을 삭제하고 일자 삭제
        days = plan.days
        for day in days:
            places = day.places
            for place in places:
                self.session.delete(place)
            self.session.delete(day)

        # 4. 플랜 삭제 후 세션 커밋
        self.session.delete(plan)
        self.session.commit()
        return {"result": 'ok'}

    # 내가 작성한 계획들 가져오기
    def get_my_plans(self, req):
        # # 사용자 계획 조회 (Eager Loading 적용)
        plans = self.session.query(Plan).options(
            joinedload(Plan.days).joinedload(Day.places)
        ).filter(Plan.writer_id == req.user_id).order_by(Plan.start_date.desc()).all()

        result = []
        for plan in plans:
            days_response = []
            for day in plan.days:
                placeResList = [PlaceResponse( place_name=place.place_name, place_visit_time=place.place_visit_time)
                          for place in day.places]
                days_response.append(DayResponse(day_number=day.day_number, places=placeResList))

            plan_response = PlanResponse(
                id=plan.id,
                writer_id=plan.writer_id,
                local_name=plan.local_name,
                start_date=plan.start_date,
                end_date=plan.end_date,
                trip_style=plan.trip_style.value,
                days=days_response,
            )
            result.append(plan_response)

        return result
