from fastapi import HTTPException, status

from fastapi import Depends

from db import get_db_session
from models import User, SignupResp, SigninResp


class UserService:
    def signup(self, user:User, db) -> SignupResp:
        # 1. ID 중복 확인
        existing_user = db.query(User).filter(User.login_id == user.login_id).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = "이미 사용 중인 아이디입니다."
            )

        # 2. 새로운 사용자 생성
        user=User(
            login_id = user.login_id,
            password = user.password,
            name = user.name
        )

        # 3. DB에 저장
        db.add(user)
        db.commit()
        db.refresh(user)

        return SignupResp(http_code=200,
                         err_msg=None)


    def signin(self, user:User, db):
        # id와 pw 검증
        db_user = (db.query(User).
                   filter(User.login_id == user.login_id)
                   .filter(User.password == user.password)
                   .first())

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="사용자가 존재하지 않거나 비밀번호가 맞지 않습니다"
            )

        res = SigninResp(http_code=200,
                   err_msg=None,
                   jwt_token=None)

        return res

