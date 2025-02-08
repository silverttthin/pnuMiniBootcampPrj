from db import get_db_session, create_db
from models import SignupResp, SigninResp
from models.User import User
from fastapi import APIRouter, Depends

from services.UserService import UserService

router = APIRouter(
    prefix="/auth",
)

@router.post("/signup")
def auth_signup(user:User,
                userService = Depends(UserService),
                db=Depends(get_db_session)) -> SignupResp:

    res = userService.signup(user,db)

    return res

@router.post("/login")
def auth_signin(user:User,
                userService = Depends(UserService),
                db=Depends(get_db_session)) -> SigninResp:
    res = userService.signin(user,db)

    return res
