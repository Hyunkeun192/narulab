from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# 🔸 사용자 요약 응답 스키마
class UserListItem(BaseModel):
    user_id: str
    nickname: str
    is_active: bool
    subscription: str
    created_at: datetime

    class Config:
        model_config = {
        "from_attributes": True
    }

# 관리자 계정 생성 요청 스키마
class AdminUserCreateRequest(BaseModel):
    email: str
    phone: str
    nickname: str
    password: str  # 미리 해시된 비밀번호 전달

    class Config:
        model_config = {
        "from_attributes": True
    }

# 🔸 관리자 역할 변경 요청 스키마
class AdminRoleUpdateRequest(BaseModel):
    role: str  # super, content, analytics

    class Config:
        model_config = {
        "from_attributes": True
    }
