from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# ✅ 사용자 탈퇴 로그 입력용 스키마
class UserDeletionLogCreate(BaseModel):
    user_id: UUID
    deleted_at: datetime
    last_company: Optional[str]
    reason: Optional[str]
