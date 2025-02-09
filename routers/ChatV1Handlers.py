﻿from fastapi import APIRouter
import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 초기화 (변경된 방식)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# FastAPI 라우터 생성
router = APIRouter()

@router.post("/chatbot/")
async def chat_with_gpt(user_input: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "넌 여행 전문가야. 사용자에게 여행 일정을 추천해줘."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}