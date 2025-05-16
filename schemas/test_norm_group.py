from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID

# 🔸 규준 등록 요청
class NormGroupCreateRequest(BaseModel):
    norm_name: str
    mean: float
    stddev: float
    level_mapping_json: Dict[str, dict]  # 예: { "STEN 1": { "min": 0, "max": 24 }, ... }
    description: Optional[str] = None

# 🔸 규준 수정 요청
class NormGroupUpdateRequest(BaseModel):
    norm_name: Optional[str] = None
    mean: Optional[float] = None
    stddev: Optional[float] = None
    level_mapping_json: Optional[Dict[str, dict]] = None
    description: Optional[str] = None

# 🔸 규준 응답 스키마
class NormGroupResponse(BaseModel):
    norm_group_id: UUID
    norm_name: str
    mean: float
    stddev: float
    level_mapping_json: Dict[str, dict]
    description: Optional[str]

    class Config:
        orm_mode = True
