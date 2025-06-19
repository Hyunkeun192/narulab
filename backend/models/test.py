import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Enum, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base
import enum

# ✅ 외부에서 Question, Option 모델 import
from backend.models.question import Question
from backend.models.option import Option

# ✅ [추가] UserTestHistory는 중복 정의 제거 후, response.py로부터 명시적 import
from backend.models.response import UserTestHistory  # 🔧 충돌 방지를 위해 직접 import

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

    question_count = Column(Integer, default=0)  # ✅ 예상 문항 수
    is_published = Column(Boolean, default=False)  # ✅ 공개 여부
    duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ 관계 설정
    questions = relationship("Question", back_populates="test")
    reports = relationship("TestReport", back_populates="test", overlaps="user_reports")
    # 🔧 수정됨: 문자열 대신 클래스 직접 참조로 변경
    user_reports = relationship(UserTestHistory, back_populates="test", overlaps="reports")

# ✅ 문항 유형 enum
class QuestionTypeEnum(str, enum.Enum):
    text = "text"
    image = "image"
    text_image = "text+image"

# ✅ 사용자 응답 테이블
class Response(Base):
    __tablename__ = "responses"

    response_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False)
    test_id = Column(String(36), ForeignKey("tests.test_id"))
    question_id = Column(String(36), ForeignKey("questions.question_id"))
    selected_option_ids = Column(JSON)
    response_time_sec = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# ✅ 검사 리포트 테이블 (분석용)
class TestReport(Base):
    __tablename__ = "test_reports"

    report_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # ✅ 사용자 ID 필드
    email = Column(String(255), nullable=False)
    test_id = Column(String(36), ForeignKey("tests.test_id"))
    score_total = Column(Float)
    score_standardized = Column(Float)
    score_level = Column(String(20))
    result_summary = Column(Text)
    report_generated_at = Column(DateTime, default=datetime.utcnow)

    # ✅ 관계 설정
    test = relationship("Test", back_populates="reports", overlaps="user_reports")
    user = relationship("User", back_populates="test_reports")
