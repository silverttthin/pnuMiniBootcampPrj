from fastapi import HTTPException, status

from fastapi import Depends

from db import get_db_session
from models import User, SignupResp, SigninResp


class UserService:
    def signup(self, user:User, db) -> SignupResp:

        user=User(
            login_id = user.login_id,
            password = user.password,
            name = user.name
        )

        db.add(user)
        db.commit()
        res = SignupResp(http_code=200,
                         err_msg=None)

        return res


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

