# app/dependencies/jwt_utils.py
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY ="1d3f771294d5db71de6b112f25d5e774"
ALG = "HS256"

class JWTUtil:
    # 1. JWT Token 생성 함수
    # Payload={
    #   "id": 1,
    #   "login_id": "loiss",
    #   "name": "aaaaa",
    #   "exp":fsdfsfsdf
    # }, 유효기간
    # -> Jwt token
    def create_token(self, payload: dict,
                    expires_delta: timedelta | None = timedelta(minutes=30)):
        payload_to_encode = payload.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        payload_to_encode.update({
            'exp': expire
        })
        return jwt.encode(payload_to_encode, SECRET_KEY, algorithm=ALG)

    # 2. token 문자열로 payload 만드는 함수
    def decode_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALG])
        except:
            pass
        return None

if __name__ == '__main__':
    payload = {
        'id': 1,
        'name': 'Linux',
        "login_id": "loiss"
    }

    jwtUtil = JWTUtil()
    token = jwtUtil.create_token(payload=payload, expires_delta=timedelta(minutes=5))
    print(token)

    payload2 = jwtUtil.decode_token(token)
    print(payload2)