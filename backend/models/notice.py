# backend/models/notice.py

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.database import Base

class Notice(Base):
    __tablename__ = "notices"

    id = Column(String(36), primary_key=True, index=True)                 # ✅ UUID 기반 고유 식별자
    title = Column(String(200), nullable=False)                           # ✅ 공지 제목
    content = Column(Text, nullable=False)                                # ✅ 공지 내용
    created_at = Column(DateTime, default=datetime.utcnow)               # ✅ 생성 시각
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ 수정 시각

    # 🔧 수정됨: 외래키 컬럼의 타입을 VARCHAR(36)으로 변경하여 users.user_id와 일치시킴
    creator_id = Column(String(36), ForeignKey("users.user_id"))          # ✅ 공지 생성자 (UUID 기반 사용자 ID 참조)

    # ✅ 관계 설정: User 모델에서 back_populates="notices"로 연결됨
    creator = relationship("User", back_populates="notices")
