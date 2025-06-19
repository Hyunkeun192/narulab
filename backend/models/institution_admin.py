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

    # 🔧 수정됨: 외래키 참조를 users.user_id로 변경하고 타입을 String(36)으로 일치시킴
    user_id = Column(String(36), ForeignKey("users.user_id"))      # ✅ UUID 기반 사용자 식별자 참조

    created_at = Column(DateTime, default=datetime.utcnow)         # ✅ 생성 시각
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ 수정 시각

    # 🔁 관계 설정은 기존 구조 유지
    # ✅ user.institution_admin으로 접근 가능하며, users.user_id 기준으로 연결됨
    user = relationship("User", backref="institution_admin")
