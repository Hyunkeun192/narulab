# backend/models/report_rule.py

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from uuid import uuid4
from backend.database.database import Base

# ✅ STEN 해석 문구 모델
class ReportRule(Base):
    __tablename__ = "report_rules"
    __table_args__ = {"extend_existing": True}

    rule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.test_id"), nullable=False)
    sten_descriptions = Column(JSONB, nullable=False)  # STEN별 해석 문구 (1~10)

    # 예시: { "1": "매우 낮음", "5": "보통", "10": "매우 높음" }
