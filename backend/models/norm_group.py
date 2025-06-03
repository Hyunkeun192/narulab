# backend/models/norm_group.py

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from uuid import uuid4
from backend.database.database import Base

# ✅ 규준 그룹 모델 정의
class NormGroup(Base):
    __tablename__ = "norm_groups"
    __table_args__ = {"extend_existing": True}

    norm_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.test_id"), nullable=False)
    group_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    rules = Column(JSONB, nullable=False)  # ✅ STEN 매핑 규칙 (점수 범위)

    # 예시:
    # rules = [
    #   { "min_score": 0, "max_score": 19, "sten": 1 },
    #   { "min_score": 20, "max_score": 39, "sten": 2 },
    #   ...
    # ]
