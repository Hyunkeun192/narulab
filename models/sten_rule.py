# narulab/models/sten_rule.py

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base
from uuid import uuid4

# ✅ 검사별 STEN 등급 구간을 저장하는 테이블
class STENRule(Base):
    __tablename__ = "sten_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)

    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.test_id"), nullable=False)  # 검사별 설정
    sten_level = Column(Integer, nullable=False)  # STEN 점수 (1~10)
    min_score = Column(Float, nullable=False)     # 이 STEN에 해당하는 점수 하한선
    max_score = Column(Float, nullable=False)     # 이 STEN에 해당하는 점수 상한선
