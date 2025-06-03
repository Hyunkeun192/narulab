# app/models/user.py

import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    encrypted_email = Column(String(255), unique=True, nullable=False)
    encrypted_phone_number = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    hashed_password = Column(TEXT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # ✅ 관리자 여부 확인용 필드 추가
    is_admin = Column(Boolean, default=False, nullable=False)

    subscription = Column(String(20), default="free", nullable=False)

    # ✅ 사용자 프로필과의 1:1 관계
    profile = relationship("UserProfile", back_populates="user", uselist=False)

    # ✅ 공지사항(Notice) 작성자와의 관계 추가
    notices = relationship("Notice", back_populates="creator")

    # ✅ 사용자 리포트(UserReport)와의 관계 추가
    reports = relationship("UserReport", back_populates="user")  # ✅ UserReport 모델에서 back_populates="user"

class UserProfile(Base):
    __tablename__ = "user_profiles"

    email = Column(String(255), primary_key=True)  # 암호화된 이메일을 FK로 사용
    school = Column(String(100))
    region = Column(String(100))
    target_company = Column(String(100))
    current_company = Column(String(100))  # 선택 입력
    age = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = Column(String(36), ForeignKey("users.user_id"))
    user = relationship("User", back_populates="profile")
