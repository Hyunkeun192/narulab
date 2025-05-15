# app/core/security.py

from passlib.context import CryptContext
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

from core.config import settings


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


# ✅ 문자열을 AES256으로 암호화
def aes_encrypt(plain_text: str) -> str:
    backend = default_backend()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=backend)
    encryptor = cipher.encryptor()

    # AES는 16바이트 블록 단위 → 패딩 필요
    padded_data = _pad(plain_text.encode(), 16)
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # base64 인코딩해서 저장/전송에 적합한 형태로 변환
    return base64.b64encode(encrypted).decode()


# ✅ AES256으로 복호화
def aes_decrypt(encoded_text: str) -> str:
    backend = default_backend()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=backend)
    decryptor = cipher.decryptor()

    decoded_data = base64.b64decode(encoded_text)
    decrypted = decryptor.update(decoded_data) + decryptor.finalize()
    return _unpad(decrypted).decode()


# 🔧 블록 단위 맞춤을 위한 패딩 함수
def _pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len] * pad_len)


# 🔧 패딩 제거 함수
def _unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]
