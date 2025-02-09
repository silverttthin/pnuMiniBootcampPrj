from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pathlib import Path

from db import get_db_session, create_db
from models import SignupResp, SigninResp
from models.User import User
from fastapi import APIRouter, Depends, FastAPI, Request

from services.UserService import UserService


#Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/auth", tags=["Auth"])

# 회원가입 페이지 렌더링 (GET 요청)
@router.get("/signup")
def signup_page(request:Request):
    return templates.TemplateResponse("signup.html", {"request":request})


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


@router.post("/logout")
async def logout():
    # response = templates.TemplateResponse("login.html", {"request":request, "msg":msgitg})
    # response.delete_cookie(key="access_token")
    return {"message":"Logged out successfully"}

