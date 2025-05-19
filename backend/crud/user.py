# app/crud/user.py

from sqlalchemy.orm import Session
from backend.models.user import User, UserProfile
from backend.schemas.user import UserCreate
from backend.core.security import hash_password
import uuid

def get_user_by_email(db: Session, encrypted_email: str):
    return db.query(User).filter(User.encrypted_email == encrypted_email).first()

# ✅ 전화번호 중복 확인용 함수 추가
def get_user_by_phone(db: Session, encrypted_phone: str):
    return db.query(User).filter(User.encrypted_phone_number == encrypted_phone).first()

def create_user(db: Session, user_data: UserCreate, encrypted_email: str, encrypted_phone: str):
    user = User(
        user_id=str(uuid.uuid4()),
        encrypted_email=encrypted_email,
        encrypted_phone_number=encrypted_phone,
        nickname=user_data.nickname,  # ✅ 사용자 입력 닉네임 저장
        hashed_password=hash_password(user_data.password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_user_profile(db: Session, user_id: str, email: str):
    profile = UserProfile(
        email=email,
        user_id=user_id,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
