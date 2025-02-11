from starlette.templating import Jinja2Templates

from dependencies.db import get_db_session
from requests.user_schema import *
from dependencies.jwt_utills import *
from fastapi import APIRouter, Depends, Request, HTTPException, Response

from services.UserService import UserService

#Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/auth", tags=["Auth"])


# 1. 회원가입 페이지 렌더링 (
@router.get("/signup/page")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# 2. 회원가입
@router.post('/signup')
def auth_signup(req: AuthSignupReq, db=Depends(get_db_session),
                jwtUtil: JWTUtil = Depends(), auth_service: UserService = Depends()):
    user = auth_service.signup(db, req)
    if not user:
        raise HTTPException(status_code=400, detail="회원가입 실패")

    # 2. 회원가입 후 JWT 토큰 발급
    # 예시로 user 정보를 그대로 토큰에 담습니다.
    jwt_token = jwtUtil.create_token(
        {
            "id": user.id,
            "user_name": user.name,
            "created_at": user.created_at,
        }
    )

    return {
        "jwt_token": jwt_token,
        "token_type": "bearer",
        "msg": "회원가입 성공"
    }


# 3. 로그인
@router.post('/signin')
def auth_signin(req: AuthSigninReq, response: Response, db=Depends(get_db_session),
                jwtUtil: JWTUtil = Depends(), auth_service: UserService = Depends()):
    jwt_token = auth_service.signin(db, jwtUtil, req)

    # 브라우저 쿠키에 토큰값 저장
    response.set_cookie(key="jwt_token", value=jwt_token)

    return {
        "jwt_token": jwt_token,
        "token_type": "bearer",
        "msg": "로그인 성공"
    }


@router.post("/logout")
async def logout(response: Response, requset: Request):
    access_token = requset.cookies.get("jwt_token")
    response.delete_cookie("jwt_token")
    # response = templates.TemplateResponse("login.html", {"request":request, "msg":msgitg})
    return {"message": "Logged out successfully"}
