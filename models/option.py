from uuid import uuid4
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base  # SQLAlchemy Base 클래스 상속

# 🔸 options 테이블 정의 (문항 선택지)
class Option(Base):
    __tablename__ = "options"

    option_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)  # 선택지 고유 ID
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False)  # 소속 문항 ID
    option_text = Column(Text, nullable=False)            # 보기 텍스트
    is_correct = Column(Boolean, default=False)           # 정답 여부
    option_image_url = Column(Text, nullable=True)        # 이미지 URL (선택)
    option_order = Column(Integer, nullable=False)        # 보기 순서 (0부터 시작)
