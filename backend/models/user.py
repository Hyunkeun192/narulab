from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base

class User(Base):
    __tablename__ = "users"

    # ✅ 기본 사용자 정보
    user_id = Column(String(36), primary_key=True, index=True)
    nickname = Column(String(50), nullable=False)

    # ✅ 이메일/전화번호 컬럼명을 DB와 일치시킴
    encrypted_email = Column(String(255), unique=True, nullable=False)  # 기존 email → 수정됨
    encrypted_phone_number = Column(String(255), unique=True, nullable=False)  # 기존 phone_number → 수정됨

    hashed_password = Column(String(255), nullable=False)

    # ✅ 활성 사용자 여부
    is_active = Column(Boolean, default=True)

    # ✅ 사용자 역할 필드 (관리자 권한 구분용)
    role = Column(String(50), nullable=False, default="user")

    # ✅ 생성/수정 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ 프로필(UserProfile)과의 관계 설정
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

