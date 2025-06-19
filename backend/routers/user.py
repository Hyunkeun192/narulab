from fastapi import APIRouter, HTTPException, Depends, Body, Query
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate, UserResponse, UserLogin
from backend.crud import user as crud_user
from backend.database.database import SessionLocal, get_db
from backend.core import security, token
from backend.models.user import User
from backend.core.security import get_current_user
from backend.models.user_deletion_log import UserDeletionLog
from datetime import datetime
from typing import Optional

router = APIRouter()

# ✅ 회원가입 API
@router.post("/api/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):

    # ⛳ 디버깅 로그
    print("🟢 [DEBUG] user_data.dict():", user_data.dict())
    print("🟢 [DEBUG] name:", user_data.name)

    if user_data.password != user_data.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    email = security.aes_encrypt(user_data.email)
    encrypted_phone = security.aes_encrypt(user_data.phone)

    existing_user = crud_user.get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")

    existing_phone = crud_user.get_user_by_phone(db, encrypted_phone)
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already exists.")

    existing_nickname = crud_user.get_user_by_nickname(db, user_data.nickname)
    if existing_nickname:
        raise HTTPException(status_code=400, detail="Nickname already exists.")

    new_user = crud_user.create_user(db, user_data, email, encrypted_phone)
    return new_user

# ✅ 로그인 API
@router.post("/api/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    email = security.aes_encrypt(user_data.email)
    user = crud_user.get_user_by_email(db, email)
    if not user or not security.verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = token.create_access_token(data={"sub": str(user.user_id)})
    refresh_token = token.create_refresh_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "refresh_token": refresh_token}

# ✅ 회원 탈퇴 API
@router.delete("/api/user/withdraw")
def withdraw_user(
    reason: str = Body(..., embed=True),  # ✅ embed=True로 명시
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = UserDeletionLog(
        user_id=current_user.user_id,
        reason=reason,
        deleted_at=datetime.utcnow(),
    )
    db.add(log)
    db.delete(current_user)
    db.commit()
    return {"message": "User successfully deleted."}

# ✅ 이메일 중복 확인 API
@router.get("/api/check-email")
def check_email_duplicate(
    email: str = Query(..., description="중복 확인할 이메일 주소"),
    db: Session = Depends(get_db)
):
    """
    사용자가 입력한 이메일이 DB에 존재하는지 암호화된 상태로 확인합니다.
    반환 형식: { "available": true } 또는 { "available": false }
    """
    email = security.aes_encrypt(email)
    user = crud_user.get_user_by_email(db, email)
    return {"available": user is None}

# ✅ 닉네임 중복 확인 API
@router.get("/api/check-nickname")
def check_nickname_duplicate(
    nickname: str = Query(..., description="중복 확인할 닉네임"),
    db: Session = Depends(get_db)
):
    """
    사용자가 입력한 닉네임이 이미 존재하는지 확인합니다.
    반환 형식: { "available": true } 또는 { "available": false }
    """
    user = crud_user.get_user_by_nickname(db, nickname)
    return {"available": user is None}

# ✅ 전화번호 중복 확인 API (📌 새로 추가됨)
@router.get("/api/check-phone")
def check_phone_duplicate(
    phone: str = Query(..., description="중복 확인할 전화번호"),
    db: Session = Depends(get_db)
):
    """
    전화번호 중복 여부 확인 API
    - 전화번호는 암호화된 상태로 비교
    - 반환 예: { "available": true } 또는 { "available": false }
    """
    encrypted_phone = security.aes_encrypt(phone)
    user = crud_user.get_user_by_phone(db, encrypted_phone)
    return {"available": user is None}

# ✅ 현재 로그인된 사용자 정보 반환 API (role 포함으로 수정됨)
@router.get("/api/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    ✅ JWT 토큰을 기반으로 현재 로그인한 사용자의 정보를 반환하는 API입니다.
    - 요청 예: GET /api/me
    - 응답: user_id, nickname, is_active 등 포함
    - 📌 관리자 권한 판단을 위해 role 추가됨
    """
    return {
        "user_id": current_user.user_id,
        "nickname": current_user.nickname,
        "is_active": current_user.is_active,
        "role": current_user.role,  # ✅ 관리자/일반 사용자 구분용으로 프론트에서 필요
        "is_admin": current_user.role != "user"  # ✅ 관리자 여부를 명시적으로 설정
    }

@router.post("/api/user/withdraw-test")
def withdraw_user_post(
    reason: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    log = UserDeletionLog(
        user_id=current_user.user_id,
        reason=reason,
        deleted_at=datetime.utcnow(),
    )
    db.add(log)
    db.delete(current_user)
    db.commit()
    return {"message": "User successfully deleted (via POST)."}