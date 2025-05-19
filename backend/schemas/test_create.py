from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID

# 🔸 검사 생성 요청 스키마
class TestCreateRequest(BaseModel):
    test_name: str                       # 검사 이름
    test_type: str                       # aptitude / personality
    version: str                         # 예: v1.0
    duration_minutes: int               # 소요 시간

# 🔸 검사 생성 응답 스키마
class TestCreateResponse(BaseModel):
    test_id: UUID                        # 생성된 검사 ID
    message: str                         # 처리 메시지
