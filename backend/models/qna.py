# backend/models/qna.py

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.database import Base

class QnA(Base):
    __tablename__ = "qna"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))

    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    is_private = Column(Boolean, default=False)

    # ✅ 정확한 테이블명 'users'로 수정
    created_by = Column(Integer, ForeignKey("users.id"))  # 🔧 수정
    answered_by = Column(Integer, ForeignKey("users.id"))  # 🔧 수정

    created_user = relationship("User", foreign_keys=[created_by], backref="qnas_created")
    answered_user = relationship("User", foreign_keys=[answered_by], backref="qnas_answered")
