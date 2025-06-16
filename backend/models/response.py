from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.database import Base
from datetime import datetime

# ✅ 사용자 개별 리포트 테이블 (검사 이력용)
class UserTestHistory(Base):
    __tablename__ = "user_reports"
    __table_args__ = {"extend_existing": True}  # ✅ 중복 정의 허용


    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)  # ✅ 기본키 (UUID 형식)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)   # ✅ 사용자 ID (FK)
    test_id = Column(String(36), ForeignKey("tests.test_id"), nullable=False)  # ✅ 검사 ID (FK)
    result_detail = Column(String, nullable=True)  # ✅ 리포트 상세 내용

    # ✅ [수정] created_at을 문자열이 아닌 DateTime으로 저장 → 쿼리 정렬 최적화
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ 생성일시 (자동 입력, UTC)

    # ✅ 사용자 관계 설정 (User.profile → UserTestHistory.user)
    user = relationship("User", back_populates="user_test_histories")

    # ✅ 검사 관계 설정 (Test.user_reports → UserTestHistory.test)
    test = relationship("Test", back_populates="user_reports", overlaps="reports,test")
