﻿import pytest
from models.chatbot import Chatbot

def test_chatbot():
    chatbot = Chatbot()
    chatbot.add_user_message("Who won the world series in 2020?")
    response = chatbot.send_request()
    assert "Dodgers" in response  # 예상되는 응답 확인