from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from backend.database.database import Base
from datetime import datetime


# ✅ 사용자 개별 리포트 테이블 (user_reports 테이블)
class UserTestHistory(Base):
    __tablename__ = "user_reports"
    __table_args__ = {"extend_existing": True}  # ✅ 중복 정의 허용

    report_id = Column(String(36), primary_key=True)  # ✅ 기본키 (UUID 문자열, MySQL은 String(36))
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # ✅ 사용자 ID (FK)
    test_id = Column(String(36), ForeignKey("tests.test_id"), nullable=False)  # ✅ 검사 ID (FK)
    result_detail = Column(String, nullable=True)  # ✅ 리포트 상세 내용
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ 생성일시 (자동 입력, UTC)

    # ✅ 사용자 관계 설정 (User.profile → UserTestHistory.user)
    user = relationship("User", back_populates="user_test_histories")

    # ✅ 검사 관계 설정 (Test.user_reports → UserTestHistory.test)
    test = relationship("Test", back_populates="user_reports", overlaps="reports,test")


# ✅ 사용자 응답 (responses 테이블)
class UserResponse(Base):
    __tablename__ = "responses"  # ✅ 실제 DB 테이블명 responses에 매핑
    __table_args__ = {"extend_existing": True}  # ✅ 중복 정의 방지

    response_id = Column(String(36), primary_key=True)  # ✅ 응답 ID (UUID 문자열)
    test_id = Column(String(36), ForeignKey("tests.test_id"), nullable=False)  # ✅ 검사 ID (FK)
    question_id = Column(String(36), ForeignKey("questions.question_id"), nullable=False)  # ✅ 문항 ID (FK)
    selected_option_ids = Column(JSON, nullable=True)  # ✅ 선택된 선택지 ID (JSON 배열)
    response_time_sec = Column(Float, nullable=True)  # ✅ 응답 소요 시간 (초)
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ 생성일시 (자동 입력)
