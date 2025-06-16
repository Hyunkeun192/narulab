from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base
import enum

# ✅ 사용자 유형 Enum
class UserRoleEnum(str, enum.Enum):
    user = "user"
    super_admin = "super_admin"
    content_admin = "content_admin"
    analytics_admin = "analytics_admin"
    company_admin = "company_admin"
    school_admin = "school_admin"

# ✅ 사용자 테이블 정의
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 기본키 → user_id로 명확하게 지정
    encrypted_email = Column(String(255), unique=True, nullable=False)  # ✅ 암호화된 이메일
    hashed_password = Column(String(255), nullable=False)  # ✅ 해시된 비밀번호
    name = Column(String(100), nullable=False)  # ✅ 이름
    nickname = Column(String(50), nullable=True)  # ✅ 닉네임
    encrypted_phone_number = Column(String(20), nullable=True)  # ✅ 암호화된 전화번호
    gender = Column(String(10), nullable=True)  # ✅ 성별
    birth_year = Column(Integer, nullable=True)  # ✅ 출생년도
    role = Column(Enum(UserRoleEnum), default="user", nullable=False)  # ✅ 사용자 권한
    is_active = Column(Boolean, default=True)  # ✅ 계정 활성 여부
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ 생성일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ 수정일시

    # ✅ 공지사항 작성자 연결 (Notice.creator → User)
    notices = relationship("Notice", back_populates="creator")

    # ✅ 사용자 개별 검사 결과 연결 (UserTestHistory.user → User)
    user_test_histories = relationship(
        "UserTestHistory", back_populates="user", overlaps="user"
    )

    # ✅ 사용자 프로필 1:1 연결 (UserProfile.user → User)
    profile = relationship(
        "UserProfile", back_populates="user", uselist=False
    )

    # ✅ 검사 리포트 연결 (TestReport.user → User)
    test_reports = relationship("TestReport", back_populates="user")  # ✅ TestReport.user_id 관계 추가됨

# ✅ 사용자 프로필 테이블 (User와 1:1 관계)
class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 기본키
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)  # ✅ 외래키 (1:1 관계)
    current_company = Column(String(100), nullable=True)  # ✅ 현재 소속 회사
    last_company = Column(String(100), nullable=True)     # ✅ 마지막 입사 회사
    education_level = Column(String(50), nullable=True)   # ✅ 학력
    experience_years = Column(Integer, nullable=True)     # ✅ 경력

    # ✅ 사용자 연결 (User.profile → UserProfile.user)
    user = relationship("User", back_populates="profile")
