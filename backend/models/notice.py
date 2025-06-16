# backend/models/notice.py

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from backend.database.database import Base

class Notice(Base):
    __tablename__ = "notices"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator_id = Column(Integer, ForeignKey("users.user_id"))  # ✅ users.id와 타입 일치
    creator = relationship("User", back_populates="notices")
