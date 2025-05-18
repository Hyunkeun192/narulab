from sqlalchemy import Column, String, Boolean, DateTime, JSON
from datetime import datetime
import uuid

from database.database import Base

class ScoringRule(Base):
    __tablename__ = "scoring_rules"

    scoring_rule_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # ✅ UUID 대신 VARCHAR(36)
    test_id = Column(String(36), nullable=False)
    scoring_key_name = Column(String(100), nullable=False)
    scoring_type = Column(String(20), nullable=False)
    is_objective = Column(Boolean, nullable=False)
    scoring_stages = Column(JSON, nullable=True)
    scoring_logic_json = Column(JSON, nullable=True)
    norm_group_id = Column(String(36), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
