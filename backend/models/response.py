# backend/models/response.py

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.database import Base
from datetime import datetime

# ✅ 사용자 리포트 결과 저장 테이블
class UserReport(Base):  # 기존: class Report(Base)
    __tablename__ = "reports"
    __table_args__ = {"extend_existing": True}

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # ✅ 외래키 수정: user_id → users.id를 참조해야 정상 동작
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.test_id"), nullable=False)

    score = Column(Integer, nullable=False)        # ✅ 정답 기반 점수 (0~100)
    sten = Column(Integer, nullable=False)         # ✅ STEN 등급 (1~10)
    description = Column(String, nullable=False)   # ✅ 해석 문구

    created_at = Column(String, default=lambda: datetime.now().isoformat())  # ✅ 문자열로 저장

    # ✅ 관계 설정
    user = relationship("User", back_populates="reports")
    test = relationship("Test", back_populates="user_reports")
