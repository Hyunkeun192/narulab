# narulab/schemas/sten_rule.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

# ✅ STEN 규칙 생성 요청 스키마
class STENRuleCreate(BaseModel):
    test_id: UUID
    sten_level: int
    min_score: float
    max_score: float

# ✅ STEN 규칙 수정 요청 스키마
class STENRuleUpdate(BaseModel):
    sten_level: Optional[int]
    min_score: Optional[float]
    max_score: Optional[float]

# ✅ STEN 규칙 응답 스키마
class STENRuleOut(BaseModel):
    id: int
    test_id: UUID
    sten_level: int
    min_score: float
    max_score: float

    class Config:
        model_config = {
        "from_attributes": True
    }
