# app/models/test.py

import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Enum, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base
import enum

# ✅ 외부에서 Question, Option 모델 import
from backend.models.question import Question
from backend.models.option import Option

# ✅ 검사 유형 enum
class TestTypeEnum(str, enum.Enum):
    aptitude = "aptitude"
    personality = "personality"

# ✅ 검사 테이블
class Test(Base):
    __tablename__ = "tests"

    test_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    test_name = Column(String(100), nullable=False)
    test_type = Column(Enum(TestTypeEnum), nullable=False)
    version = Column(String(20), nullable=False)
    version_note = Column(Text)

    # ✅ [추가] 예상 문항 수 저장 필드
    question_count = Column(Integer, default=0)  # 관리자 입력 기반 문항 수

    # ✅ [추가] 완성 검사 여부 표시 (True일 때 product 페이지에 노출)
    is_published = Column(Boolean, default=False)

    duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ 관계 설정: 문항/옵션/리포트와 연결
    questions = relationship("Question", back_populates="test")
    reports = relationship("TestReport", back_populates="test")  # ✅ Report → TestReport

    # ✅ [추가] 사용자 리포트 연결을 위한 관계 필드
    user_reports = relationship("UserReport", back_populates="test")  # ✅ UserReport 모델 연결용


# ✅ 문항 유형 enum (예: 텍스트, 이미지 등)
class QuestionTypeEnum(str, enum.Enum):
    text = "text"
    image = "image"
    text_image = "text+image"


# ✅ 사용자 응답 테이블
class Response(Base):
    __tablename__ = "responses"

    response_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False)  # FK → users.email (암호화된 값)
    test_id = Column(String(36), ForeignKey("tests.test_id"))
    question_id = Column(String(36), ForeignKey("questions.question_id"))
    selected_option_ids = Column(JSON)  # ✅ 복수 선택 대응
    response_time_sec = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


# ✅ 검사 리포트 테이블
class TestReport(Base):  # ✅ 기존: class Report(Base)
    __tablename__ = "reports"

    report_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False)  # FK → users.email (암호화된 값)
    test_id = Column(String(36), ForeignKey("tests.test_id"))
    score_total = Column(Float)
    score_standardized = Column(Float)
    score_level = Column(String(20))  # 예: STEN 7
    result_summary = Column(Text)
    report_generated_at = Column(DateTime, default=datetime.utcnow)

    # ✅ 관계 설정: 검사(Test)와 연결
    test = relationship("Test", back_populates="reports")
