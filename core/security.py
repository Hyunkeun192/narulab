# app/core/security.py

from passlib.context import CryptContext
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

from core.config import settings

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User

# 🔐 bcrypt를 활용한 비밀번호 해시 및 검증을 위한 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ 비밀번호를 bcrypt 방식으로 해시
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ✅ 해시된 비밀번호와 사용자가 입력한 비밀번호를 비교
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 🛡 AES256 양방향 암호화를 위한 키 설정
# (환경변수 또는 .env에서 읽어오되, 여기선 예시 키를 생성)
AES_KEY = settings.AES_SECRET_KEY[:32].encode()  # ✅ AES 전용 키 사용
AES_IV = AES_KEY[:16]  # CBC 모드 초기화 벡터 (보통 고정값 사용 가능)


# ✅ AES256 CBC 모드 기반 암호화
def aes_encrypt(plain_text: str) -> str:
    backend = default_backend()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=backend)
    encryptor = cipher.encryptor()
    padded_data = plain_text.encode() + b"\0" * (16 - len(plain_text.encode()) % 16)
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted).decode()


# ✅ 복호화 함수
def aes_decrypt(encrypted_text: str) -> str:
    backend = default_backend()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=backend)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(base64.b64decode(encrypted_text)) + decryptor.finalize()
    return decrypted.rstrip(b"\0").decode()


# ✅ 현재 로그인된 사용자 정보 가져오기 (JWT 기반)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")  # 🔑 토큰 경로 설정

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    JWT access token을 기반으로 현재 로그인된 사용자 정보를 반환합니다.
    유효하지 않거나 비활성화된 사용자는 예외 처리합니다.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")

    return user
