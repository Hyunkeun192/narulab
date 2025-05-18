from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Any
from datetime import datetime

# 🔸 채점 기준 등록 요청
class ScoringRuleCreateRequest(BaseModel):
    test_id: UUID
    scoring_key_name: str
    scoring_type: str  # likert / ipsative / custom
    is_objective: bool
    scoring_stages: Optional[int] = None
    scoring_logic_json: dict
    norm_group_id: Optional[UUID] = None
    description: Optional[str] = None

# 🔸 채점 기준 수정 요청
class ScoringRuleUpdateRequest(BaseModel):
    scoring_key_name: Optional[str] = None
    scoring_type: Optional[str] = None
    is_objective: Optional[bool] = None
    scoring_stages: Optional[int] = None
    scoring_logic_json: Optional[dict] = None
    norm_group_id: Optional[UUID] = None
    description: Optional[str] = None

# 🔸 채점 기준 응답 스키마
class ScoringRuleResponse(BaseModel):
    scoring_rule_id: UUID
    test_id: UUID  # ✅ 누락되어 있던 필드 보완
    scoring_key_name: str
    scoring_type: str
    is_objective: bool
    scoring_stages: Optional[int]
    scoring_logic_json: Optional[dict]  # ✅ 누락되어 있던 필드 보완
    norm_group_id: Optional[UUID]
    description: Optional[str]
    created_at: datetime  # ✅ 생성일자 필드 보완

    class Config:
        orm_mode = True
