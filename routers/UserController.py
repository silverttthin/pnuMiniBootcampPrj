from sqlmodel import Session
from starlette.templating import Jinja2Templates

from dependencies.db import get_db_session
from requests.user_schema import *
from dependencies.jwt_utills import *
from fastapi import APIRouter, Depends, Request, HTTPException

from services.UserService import UserService


#Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/auth", tags=["Auth"])

# 회원가입 페이지 렌더링 (GET 요청)
@router.get("/signup")
def signup_page(request:Request):
    return templates.TemplateResponse("signup.html", {"request":request})


@router.post('/signup')
def auth_signup(req: AuthSignupReq,
                db = Depends(get_db_session),
                jwtUtil:JWTUtil=Depends(),     # 클래스
                auth_service:UserService=Depends()):
    user = auth_service.signup(db, req.login_id, req.pwd, req.name)
    if not user:
        raise HTTPException(status_code=400,
                      detail="회원가입실패")

    # 2. 회원가입 후 JWT 토큰 발급
    # 예시로 user 정보를 그대로 토큰에 담습니다.
    access_token = jwtUtil.create_token(user.model_dump())

    # 3. 발급된 토큰을 DB에 저장
    user.access_token = access_token
    db.commit()  # 변경사항 저장
    db.refresh(user)

    return {
        "jwt_token" :user.access_token,
        "err_msg": "회원가입 성공"
    }

# 2. signin
@router.post('/signin')
def auth_signin(req: AuthSigninReq,
                db = Depends(get_db_session),  # 함수
                jwtUtil:JWTUtil=Depends(),     # 클래스
                auth_service:UserService=Depends()):
    user = auth_service.signin(db, req.login_id, req.pwd)
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")

    user.access_token = jwtUtil.create_token(user.model_dump())

    return {
        "jwt_token" :user.access_token,
        "err_msg": "로그인 성공"
    }



@router.post("/logout")
async def logout():
    # response = templates.TemplateResponse("login.html", {"request":request, "msg":msgitg})
    # response.delete_cookie(key="access_token")
    return {"message":"Logged out successfully"}

