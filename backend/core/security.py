# app/core/security.py

from passlib.context import CryptContext
from Crypto.Cipher import AES  # ✅ 변경: cryptography 대신 pycryptodome 사용
import base64
import hashlib

from backend.core.config import settings

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models.user import User

# 🔐 bcrypt를 활용한 비밀번호 해시 및 검증을 위한 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 비밀번호를 bcrypt 방식으로 해시
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ 해시된 비밀번호와 사용자가 입력한 비밀번호를 비교
def verify_password(plain_password: str, password: str) -> bool:
    return pwd_context.verify(plain_password, password)

# ✅ AES 암호화 키 준비 (32바이트 키로 SHA256 변환)
AES_SECRET_KEY = settings.AES_SECRET_KEY  # .env에서 불러옴

# ✅ Codex와 동일한 AES-256 + ECB + PKCS7 padding 방식으로 암호화
def aes_encrypt(plain_text: str) -> str:
    key = hashlib.sha256(AES_SECRET_KEY.encode()).digest()  # 32바이트 키로 변환
    cipher = AES.new(key, AES.MODE_ECB)
    pad_len = 16 - len(plain_text.encode()) % 16
    padded = plain_text + chr(pad_len) * pad_len
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted).decode()

# ✅ Codex와 동일한 방식의 복호화
def aes_decrypt(encrypted_text: str) -> str:
    key = hashlib.sha256(AES_SECRET_KEY.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_text))
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode()

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
