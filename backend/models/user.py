from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base
import enum

# ✅ 중복 정의 충돌 방지를 위해 명시적으로 클래스 import
from backend.models.response import UserTestHistory

# ✅ 사용자 유형 Enum
class UserRoleEnum(str, enum.Enum):
    user = "user"
    super_admin = "super_admin"
    content_admin = "content_admin"
    analytics_admin = "analytics_admin"
    company_admin = "company_admin"
    school_admin = "school_admin"

# ✅ 사용자 테이블 정의 (DB 기준으로 수정 완료됨)
class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True)  # ✅ UUID 문자열로 기본키 설정

    email = Column(String(255), unique=True, nullable=False)  # ✅ [수정] 암호화된 이메일 → 일반 email
    password = Column(String(255), nullable=False)  # ✅ [수정] password → password
    name = Column(String(100), nullable=False)  # ✅ 이름
    nickname = Column(String(50), nullable=True)  # ✅ 닉네임
    phone = Column(String(20), nullable=True)  # ✅ [수정] phone → phone
    gender = Column(String(10), nullable=True)  # ✅ 성별
    birth_year = Column(Integer, nullable=True)  # ✅ 출생년도
    role = Column(Enum(UserRoleEnum), default="user", nullable=False)  # ✅ 사용자 권한
    is_active = Column(Boolean, default=True)  # ✅ 계정 활성 여부
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ 생성일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ 수정일시

    # ✅ 공지사항 작성자 연결 (Notice.creator → User)
    notices = relationship("Notice", back_populates="creator")

    # ✅ 사용자 검사 이력 (UserTestHistory.user → User)
    user_test_histories = relationship(
        UserTestHistory, back_populates="user", overlaps="user"
    )

    # ✅ 사용자 프로필 1:1 연결 (UserProfile.user → User)
    profile = relationship(
        "UserProfile", back_populates="user", uselist=False
    )

    # ✅ 검사 리포트 연결 (TestReport.user → User)
    test_reports = relationship("TestReport", back_populates="user", lazy="raise")


# ✅ 사용자 프로필 테이블 (User와 1:1 관계)
class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 기본키

    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False, unique=True)  # ✅ UUID 외래키

    current_company = Column(String(100), nullable=True)  # ✅ 현재 소속 회사
    last_company = Column(String(100), nullable=True)     # ✅ 마지막 입사 회사
    education_level = Column(String(50), nullable=True)   # ✅ 학력
    experience_years = Column(Integer, nullable=True)     # ✅ 경력

    # ✅ 관계 설정 (User.profile → UserProfile.user)
    user = relationship("User", back_populates="profile")
