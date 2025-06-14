# backend/models/notice.py

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.database import Base

class Notice(Base):
    __tablename__ = "notices"

    id = Column(String(36), primary_key=True, index=True)  # ✅ UUID 문자열 기반 기본키
    title = Column(String(200), nullable=False)  # ✅ 공지 제목
    content = Column(Text, nullable=False)  # ✅ 공지 내용

    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ 생성 일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ 수정 일시

    # ✅ 작성자 ID (users 테이블의 id와 연결, 기존 user_id에서 id로 수정)
    creator_id = Column(String(36), ForeignKey("users.id"))

    # ✅ User 모델과의 관계 설정 (작성자)
    creator = relationship("User", back_populates="notices")
