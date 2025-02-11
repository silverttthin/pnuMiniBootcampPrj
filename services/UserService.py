import time
from fastapi import HTTPException
from sqlmodel import Session, select

from dependencies.jwt_utills import JWTUtil
from models import User
import bcrypt

from requests.user_schema import AuthSignupReq, AuthSigninReq


def get_user_by_name(db: Session, login_id: str) -> User | None:
    stmt = select(User).where(User.login_id == login_id)
    results = db.exec(stmt)
    for user in results:
        return user
    return None


# Password 단방향 암호화 함수
def get_hashed_pwd(password: str):
    encoded_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_password, salt)  # salt를 해싱 패스워드에 포함시킴


# 사용자 입력 password와 디비에 저장된 해싱 password 검증
def verify_pwd(password: str, hashed_password: bytes) -> bool:
    encoded_password = password.encode('utf-8')  # string -> byte
    return bcrypt.checkpw(password=encoded_password, hashed_password=hashed_password)


class UserService:
    # 회원가입
    def signup(self, db: Session, req: AuthSignupReq) -> User | None:
        try:
            # 1. 암호화된 패스워드 생성
            hashed_pwd = get_hashed_pwd(req.password)
            # 2. 입력 정보 포함된 User 객체 만들어 insert
            user = User(login_id=req.login_id, password=hashed_pwd, name=req.name, created_at=int(time.time()))
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        except Exception as e:
            print(f'회원가입 실패!! -> {e}')
            return None

    # 로그인
    def signin(self, db: Session, jwtUtil: JWTUtil, req: AuthSigninReq):
        user = get_user_by_name(db, req.login_id)
        # 존재하지 않는 id거나 비밀번호가 다르면
        if not user or not verify_pwd(req.password, user.password):
            raise HTTPException(status_code=400, detail="로그인 정보를 확인해주세요")

        jwt_token = jwtUtil.create_token(
            {
                "id": user.id,
                "username": user.name,
                "created_at": user.created_at,
            }
        )
        return jwt_token

    # 토큰에서 페이로드 추출
    def get_payload(self, jwt_token: str, jwtUtil: JWTUtil) -> dict:
        if jwt_token is None:
            raise HTTPException(status_code=400, detail="토큰이 존재하지 않습니다")
        payload = jwtUtil.decode_token(jwt_token)
        return payload
