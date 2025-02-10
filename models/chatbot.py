#chatbot 클래스 구현

from dependencies.chat_utils import get_openai_client
from dependencies.config import OPENAI_MODEL

class Chatbot:
    def __init__(self):
        """초기화: context 데이터를 만들고 시스템 역할을 설정"""
        self.context = [{"role": "system", "content": "You are a helpful assistant."}]
        self.client = get_openai_client()
        self.model = OPENAI_MODEL

    def add_user_message(self, message: str):
        """사용자 메시지를 context 데이터에 추가"""
        self.context.append({"role": "user", "content": message})

    def send_request(self):
        """현재 context를 OpenAI API에 전송하여 응답 받기"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.context
        ).model_dump()
        return response["choices"][0]["message"]["content"]

    def add_response(self, response: str):
        """응답 내용을 context 데이터에 추가"""
        self.context.append({"role": "assistant", "content": response})

    def get_response(self):
        """응답 내용을 반환"""
        return self.context[-1]["content"]