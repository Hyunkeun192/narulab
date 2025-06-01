# app/routers/user.py

from fastapi import APIRouter, HTTPException, Depends, Body, Query  # ✅ Query import 추가
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

    # ✅ 2. 이메일, 전화번호 암호화
    encrypted_email = security.aes_encrypt(user_data.email)
    encrypted_phone = security.aes_encrypt(user_data.phone_number)

    # ✅ 3. 중복 확인 (이메일)
    existing_user = crud_user.get_user_by_email(db, encrypted_email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")

    # ✅ 4. 중복 확인 (전화번호)
    existing_phone = crud_user.get_user_by_phone(db, encrypted_phone)
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already exists.")

    # ✅ 5. 닉네임 중복 확인
    if crud_user.get_user_by_nickname(db, user_data.nickname):
        raise HTTPException(status_code=400, detail="Nickname already exists.")

    # ✅ 6. 유저 생성
    user = crud_user.create_user(db, user_data, encrypted_email, encrypted_phone)
    return user

# ✅ 닉네임 중복 확인 라우트
@router.get("/api/users/check-nickname")
def check_nickname(nickname: str = Query(...), db: Session = Depends(get_db)):
    """
    ✅ 닉네임 중복 여부 확인 API
    - 클라이언트는 닉네임 입력 후 이 API로 사용 가능 여부 확인
    - 예시 요청: GET /api/users/check-nickname?nickname=하마777
    - 응답: {"available": true} 또는 {"available": false}
    """
    existing_user = crud_user.get_user_by_nickname(db, nickname=nickname)
    return {"available": existing_user is None}

# ✅ 🔽 [추가] 전화번호 중복 확인 라우트
@router.get("/api/users/check-phone")
def check_phone(phone: str = Query(...), db: Session = Depends(get_db)):
    """
    ✅ 전화번호 중복 여부 확인 API
    - 요청 예시: GET /api/users/check-phone?phone=010-1234-5678
    - 반환값: {"available": true} 또는 {"available": false}
    """
    encrypted_phone = security.aes_encrypt(phone)
    user = crud_user.get_user_by_phone(db, encrypted_phone)
    return {"available": user is None}

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

# ✅ 이메일 중복 확인 API (프론트 회원가입 시 사용)
@router.get("/api/users/check-email")
def check_email_duplicate(
    email: str = Query(..., description="중복 확인할 이메일 주소"),
    db: Session = Depends(get_db)
):
    """
    사용자가 입력한 이메일이 DB에 존재하는지 암호화된 상태로 확인합니다.
    반환 형식: { "available": true } 또는 { "available": false }
    """
    encrypted_email = security.aes_encrypt(email)
    user = crud_user.get_user_by_email(db, encrypted_email)
    return {"available": user is None}

# ✅ 현재 로그인된 사용자 정보 반환 API
@router.get("/api/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    ✅ JWT 토큰을 기반으로 현재 로그인한 사용자의 정보를 반환하는 API입니다.
    - 요청 예: GET /api/me
    - 응답: user_id, nickname, is_active 등 포함
    """
    return current_user
