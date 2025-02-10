# 공통 의존성( OpenAI API, Redis 연결 등등)
from openai import OpenAI
from dependencies.config import OPENAI_API_KEY

# OpenAI API 클라이언트 생성
client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_client():
    return client
