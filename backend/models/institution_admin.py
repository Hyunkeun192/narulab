# backend/models/institution_admin.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime  # ✅ SQLAlchemy 기본 컬럼/제약조건 타입
from sqlalchemy.orm import relationship  # ✅ 관계 설정
from backend.database.database import Base  # ✅ SQLAlchemy Base 클래스
from datetime import datetime  # ✅ 생성/수정 시간용
from uuid import uuid4  # ✅ 향후 사용할 가능성이 있으므로 반드시 유지

class InstitutionAdmin(Base):
    __tablename__ = "institution_admins"  # ✅ 실제 테이블 이름 지정

    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 고유 기본키, 자동 증가 정수형

    email = Column(String(255), unique=True, nullable=False)       # ✅ 관리자 이메일
    name = Column(String(100), nullable=False)                     # ✅ 관리자 이름
    institution_type = Column(String(50), nullable=False)          # ✅ 기관 종류 (예: 학교, 기업)
    institution_name = Column(String(100), nullable=False)         # ✅ 기관 이름

    # 🔧 ForeignKey 수정됨: 기존 users.user_id → users.id (User 모델 통일 기준에 맞춤)
    user_id = Column(Integer, ForeignKey("users.id"))              # ✅ 사용자 테이블의 id 참조

    created_at = Column(DateTime, default=datetime.utcnow)         # ✅ 생성 시각
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ 수정 시각

    # ✅ 관계 설정: User → InstitutionAdmin
    user = relationship("User", backref="institution_admin")       # ✅ user.institution_admin 역참조 가능
