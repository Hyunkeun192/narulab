from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.database.database import Base
from uuid import uuid4  # ✅ 추가

class Notice(Base):
    __tablename__ = "notices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # ✅ UUID 자동 생성
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String(36), ForeignKey("users.user_id"))

    creator = relationship("User", back_populates="notices")
