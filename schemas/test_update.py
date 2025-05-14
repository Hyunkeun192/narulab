from pydantic import BaseModel
from typing import Optional
from uuid import UUID

# 🔸 검사 수정 요청 스키마
class TestUpdateRequest(BaseModel):
    test_name: Optional[str] = None             # 검사명 (선택 수정)
    test_type: Optional[str] = None             # 검사 유형 (aptitude / personality)
    version: Optional[str] = None               # 버전
    duration_minutes: Optional[int] = None      # 소요 시간
    scoring_rule_id: Optional[UUID] = None      # 채점 기준 연결
    norm_group_id: Optional[UUID] = None        # 규준 연결

# 🔸 검사 수정 응답 스키마
class TestUpdateResponse(BaseModel):
    test_id: UUID
    message: str
