# app/crud/user.py

from sqlalchemy.orm import Session
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate
from app.core.security import hash_password
import uuid


def get_user_by_email(db: Session, encrypted_email: str):
    return db.query(User).filter(User.encrypted_email == encrypted_email).first()


def create_user(db: Session, user_data: UserCreate, encrypted_email: str, encrypted_phone: str):
    user = User(
        user_id=str(uuid.uuid4()),
        encrypted_email=encrypted_email,
        encrypted_phone_number=encrypted_phone,
        nickname=f"진로탐험가{str(uuid.uuid4())[:6]}",
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
