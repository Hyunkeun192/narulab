# backend/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"  # ✅ 실제 테이블 이름은 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 🔧 기존 user_id → id 로 변경 (qna.py 외래키 대응)

    email = Column(String(255), unique=True, nullable=False)  # 사용자 이메일
    password = Column(String(255), nullable=False)            # 비밀번호 해시값
    name = Column(String(100), nullable=False)                # 이름
    nickname = Column(String(50), nullable=True)              # 닉네임
    phone = Column(String(20), nullable=True)                 # 휴대폰 번호
    gender = Column(String(10), nullable=True)                # 성별
    birth_year = Column(Integer, nullable=True)               # 출생 연도

    role = Column(String(50), nullable=False, default="user") # 사용자 권한 (예: user, super_admin 등)
    is_active = Column(Boolean, default=True)                 # 활성 상태 여부

    # ✅ 생성/수정 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ 프로필(UserProfile)과의 관계 설정
    profile = relationship("UserProfile", back_populates="user", uselist=False)

    # ✅ 공지사항(Notice) 작성자와의 관계 추가
    notices = relationship("Notice", back_populates="creator")

    # ✅ 사용자 리포트(UserReport)와의 관계 추가
    reports = relationship("UserReport", back_populates="user")  # ✅ UserReport 모델에서 back_populates="user"

    # ✅ 관리자 여부 판단 프로퍼티 추가 (super_admin, content_admin, analytics_admin 포함)
    @property
    def is_admin(self):
        return self.role in ['super_admin', 'content_admin', 'analytics_admin']


class UserProfile(Base):
    __tablename__ = "user_profiles"

    email = Column(String(255), primary_key=True)             # 암호화된 이메일을 기본키로 사용
    school = Column(String(100))                              # 학교
    region = Column(String(100))                              # 지역
    target_company = Column(String(100))                      # 목표 기업
    current_company = Column(String(100))                     # 현재 회사 (선택)
    age = Column(Integer)                                     # 나이
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 최종 수정일

    user_id = Column(Integer, ForeignKey("users.id"))         # 🔧 기존 users.user_id → users.id 로 변경
    user = relationship("User", back_populates="profile")     # 역방향 관계 설정
