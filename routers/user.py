# app/routers/user.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse, UserLogin  # ✅ 로그인 모델 추가 import
from crud import user as crud_user
from database.database import SessionLocal
from core import security, token  # 🔐 보안/토큰 유틸

router = APIRouter()

# ✅ DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 회원가입 API
@router.post("/api/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # ✅ 1. 비밀번호 일치 여부 확인
    if user_data.password != user_data.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    # 2. 이메일, 전화번호 암호화
    encrypted_email = security.aes_encrypt(user_data.email)
    encrypted_phone = security.aes_encrypt(user_data.phone_number)

    # 3. 중복 확인 (이메일)
    existing_user = crud_user.get_user_by_email(db, encrypted_email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")

    # ✅ 4. 중복 확인 (전화번호)
    existing_phone = crud_user.get_user_by_phone(db, encrypted_phone)
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already exists.")

    # 5. 사용자 생성
    user = crud_user.create_user(db, user_data, encrypted_email, encrypted_phone)
    crud_user.create_user_profile(db, user.user_id, encrypted_email)

    # 6. 응답 반환
    return UserResponse(
        user_id=user.user_id,
        email=user_data.email,
        nickname=user.nickname,
        is_active=user.is_active
    )

# ✅ 로그인 API
@router.post("/api/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):  # ✅ 모델 변경
    # 1. 이메일 암호화
    encrypted_email = security.aes_encrypt(user_data.email)

    # 2. 사용자 조회 및 비밀번호 검증
    user = crud_user.get_user_by_email(db, encrypted_email)
    if not user or not security.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # 3. JWT 토큰 생성
    access_token = token.create_access_token(data={"user_id": user.user_id})
    refresh_token = token.create_refresh_token(data={"user_id": user.user_id})

    # 4. 토큰 반환
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
