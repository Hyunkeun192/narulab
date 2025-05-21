# app/routers/user.py

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate, UserResponse, UserLogin  # ✅ 로그인 모델 추가 import
from backend.crud import user as crud_user
from backend.database.database import SessionLocal, get_db
from backend.core import security, token  # 🔐 보안/토큰 유틸
from backend.models.user import User
from backend.core.security import get_current_user  # ✅ 현재 로그인 유저 확인용 의존성
from backend.models.user_deletion_log import UserDeletionLog  # ✅ 사용자 탈퇴 로그 모델 import
from datetime import datetime
from typing import Optional

router = APIRouter()

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

    # 5. 유저 생성 - 암호화된 이메일과 전화번호를 전달
    user = crud_user.create_user(db, user_data, encrypted_email, encrypted_phone)

    return user

# ✅ 로그인 API
@router.post("/api/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    encrypted_email = security.aes_encrypt(user_data.email)
    user = crud_user.get_user_by_email(db, encrypted_email)
    if not user or not security.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = token.create_access_token(data={"sub": str(user.user_id)})
    refresh_token = token.create_refresh_token(data={"sub": str(user.user_id)})

    return {"access_token": access_token, "refresh_token": refresh_token}

# ✅ 사용자 탈퇴 API (탈퇴 로그 저장 포함)
@router.delete("/api/users/me")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    deletion_reason: Optional[str] = Body(None),       # ✅ 탈퇴 사유 (선택 입력)
    last_company: Optional[str] = Body(None)           # ✅ 마지막 소속 회사 (선택 입력)
):
    # ✅ 탈퇴 로그 저장
    log = UserDeletionLog(
        user_id=current_user.user_id,
        deleted_at=datetime.utcnow(),
        reason=deletion_reason,
        last_company=last_company
    )
    db.add(log)

    # ✅ 실제 계정 비활성화 처리
    current_user.is_active = False
    db.commit()

    return {"message": "Your account has been deactivated and deletion has been logged."}
