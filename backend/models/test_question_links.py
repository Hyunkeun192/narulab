# backend/models/test_question_links.py

import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from backend.database.database import Base

# ✅ 검사와 문항을 연결하는 중간 테이블 모델
class TestQuestionLink(Base):
    __tablename__ = "test_question_links"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # 연결될 검사 ID
    test_id = Column(String(36), ForeignKey("tests.test_id"), nullable=False)

    # 연결될 문항 ID
    question_id = Column(String(36), ForeignKey("questions.question_id"), nullable=False)

    # 검사 내 문항 순서
    order_index = Column(Integer, nullable=True)

    # 생성 일시
    created_at = Column(DateTime, default=datetime.utcnow)
