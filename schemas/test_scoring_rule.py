from pydantic import BaseModel
from uuid import UUID
from typing import Optional

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
    scoring_key_name: str
    scoring_type: str
    is_objective: bool
    scoring_stages: Optional[int]
    norm_group_id: Optional[UUID]
    description: Optional[str]

    class Config:
        orm_mode = True
