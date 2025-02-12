#OpenAI 서비스 로직

from dependencies import get_openai_client
from dependencies.config import OPENAI_MODEL

def chat_with_openai(context):
    """OpenAI API에 context를 전송하고 응답을 반환"""
    client = get_openai_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=context
    ).model_dump()
    return response["choices"][0]["message"]["content"]