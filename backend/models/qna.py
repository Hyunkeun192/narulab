from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from backend.database.database import Base
from uuid import uuid4

class QnA(Base):
    __tablename__ = "qna"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)

    created_by = Column(String(36), ForeignKey("users.user_id"))
    created_at = Column(DateTime, server_default=func.now())

    answered_by = Column(String(36), ForeignKey("users.user_id"), nullable=True)
    answered_at = Column(DateTime, nullable=True)
