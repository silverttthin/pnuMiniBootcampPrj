import os

from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

class JWTUtil:

    # 사용자가 입력한 페이로드에 만료기한을 넣어 인코딩해 JWT 토큰값을 리턴
    def create_token(self, payload: dict,
                     expires_delta: timedelta | None = timedelta(minutes=30)):
        try:
            payload_to_encode = payload.copy()  # copy는 안써도 되는데 추후 원본 payload 활용할 수 있으므로 사용
            expire = datetime.now(timezone.utc) + expires_delta
            payload_to_encode.update({'exp': expire})
            return jwt.encode(payload_to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALG"))

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Token Encoding Failed! : {str(e)}")

    # token 문자열로 payload 만드는 함수
    def decode_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALG")])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Token Decoding Failed! : {str(e)}")
