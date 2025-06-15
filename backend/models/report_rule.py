# backend/models/report_rule.py

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import JSON  # ✅ MySQL에서 지원하는 JSON 타입 사용
from uuid import uuid4
from backend.database.database import Base

# ✅ STEN 해석 문구 모델
class ReportRule(Base):
    __tablename__ = "report_rules"
    __table_args__ = {"extend_existing": True}

    rule_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # ✅ UUID 문자열로 변경
    test_id = Column(String(36), ForeignKey("tests.test_id"), nullable=False)  # ✅ ForeignKey도 문자열 기반
    sten_descriptions = Column(JSON, nullable=False)  # ✅ MySQL 호환 JSON 타입
    # 예시: { "1": "매우 낮음", "5": "보통", "10": "매우 높음" }
