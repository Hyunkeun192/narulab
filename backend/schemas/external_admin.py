from pydantic import BaseModel
from typing import Literal, Any

# 🔸 외부 관리자 등록 요청
class ExternalAdminCreateRequest(BaseModel):
    user_id: str
    institution_type: Literal["school", "company"]
    institution_name: str

# 🔸 승인/거절 처리 요청
class ExternalAdminApprovalRequest(BaseModel):
    approved: bool
