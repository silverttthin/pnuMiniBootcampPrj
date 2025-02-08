from http.client import HTTPException

from fastapi import Depends

from db import get_db_session
from models import User, SignupResp


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
