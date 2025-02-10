from pydantic import BaseModel, Field


class SignupResp(BaseModel):
    err_msg:str|None=None
    http_code:int|None=None

class SigninResp(BaseModel):
    jwt_token:str|None=None
    err_msg:str|None=None
    http_code:int|None=None

class AuthSigninReq(BaseModel):
    login_id: str
    pwd: str

class AuthSignupReq(BaseModel):
    login_id: str
    pwd: str
    name: str