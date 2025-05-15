import enum
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, String, Text, Boolean, Enum as PgEnum, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base  # SQLAlchemy Base 클래스 상속

# 🔸 문항 상태 정의 (승인 대기/승인/반려)
class QuestionStatus(str, enum.Enum):
    waiting = "waiting"
    approved = "approved"
    rejected = "rejected"

# 🔸 questions 테이블 정의
class Question(Base):
    __tablename__ = "questions"

    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)  # 고유 문항 ID
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.test_id"), nullable=False)  # 어떤 검사에 속한 문항인지
    question_type = Column(String, nullable=False)         # 문항 유형 (text / image 등)
    question_text = Column(Text, nullable=True)            # 질문 텍스트
    question_image_url = Column(Text, nullable=True)       # 질문 이미지 URL (선택)
    is_multiple_choice = Column(Boolean, default=False)    # 복수 선택 여부
    order_index = Column(Integer, nullable=True)           # 문항 순서 (선택)

    # 🔸 AI 문항 승인/반려 기능을 위한 필드
    status = Column(PgEnum(QuestionStatus), default=QuestionStatus.waiting, nullable=False)  # 상태: 승인/반려/대기
    review_comment = Column(Text, nullable=True)                                              # 반려 시 코멘트

    # 🔸 생성일시 (목록 정렬용)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # 생성 시각
