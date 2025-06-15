from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base
import enum

# ✅ 사용자 권한 유형 enum
class UserRoleEnum(str, enum.Enum):
    user = "user"
    super_admin = "super_admin"
    content_admin = "content_admin"
    analytics_admin = "analytics_admin"
    external_admin = "external_admin"

# ✅ 사용자 테이블 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 기본키 (자동 증가 정수형)
    email = Column(String(255), unique=True, nullable=False)    # ✅ 이메일 (암호화 저장)
    hashed_password = Column(String(255), nullable=False)       # ✅ 해시된 비밀번호
    name = Column(String(100), nullable=False)                  # ✅ 이름
    nickname = Column(String(50), nullable=True)                # ✅ 닉네임
    phone = Column(String(20), nullable=True)                   # ✅ 전화번호 (암호화 저장)
    gender = Column(String(10), nullable=True)                  # ✅ 성별
    birth_year = Column(Integer, nullable=True)                 # ✅ 출생년도
    role = Column(Enum(UserRoleEnum), default="user", nullable=False)  # ✅ 사용자 역할
    is_active = Column(Boolean, default=True)                   # ✅ 활성 여부
    created_at = Column(DateTime, default=datetime.utcnow)      # ✅ 생성 일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ 수정 일시

    # ✅ 공지사항 작성자 관계 (Notice.creator → User)
    notices = relationship("Notice", back_populates="creator")

    # ✅ 사용자 리포트 결과 연결 (UserTestHistory.user → User)
    user_test_histories = relationship(
        "UserTestHistory", back_populates="user", overlaps="user"
    )  # ✅ 검사 이력 관계 (이름 변경 후 충돌 방지용 overlaps 추가)
