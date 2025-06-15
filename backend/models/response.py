from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.database import Base
from datetime import datetime

# ✅ 사용자 개별 리포트(검사 이력) 테이블
class UserTestHistory(Base):
    __tablename__ = "user_test_histories"
    __table_args__ = {"extend_existing": True}

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.test_id"), nullable=False)

    score = Column(Integer, nullable=False)
    sten = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.now().isoformat())

    # ✅ 관계 설정
    user = relationship("User", back_populates="user_test_histories")
    test = relationship("Test", back_populates="user_test_histories", overlaps="reports")
