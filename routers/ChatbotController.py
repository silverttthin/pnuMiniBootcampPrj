﻿from fastapi import APIRouter, Depends, Form, Request
from starlette.templating import Jinja2Templates

from models.chatbot import Chatbot

templates = Jinja2Templates(directory="templates")
router = APIRouter() 

@router.post("/message")
async def chat(
    user_input: str = Form(...),  # 폼(Form)으로부터 문자열 하나 받기
    chatbot=Depends(Chatbot)
):
    chatbot.add_user_message(user_input)
    response = chatbot.send_request()
    chatbot.add_response(response)
    return {"response": chatbot.get_response()}
