from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Request
from pathlib import Path


router = APIRouter()

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 홈 페이지 라우트
@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})