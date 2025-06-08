# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional, Any

# ✅ 회원가입 요청용
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str  # ✅ 비밀번호 확인 추가
    phone_number: str
    nickname: str  # ✅ 닉네임 직접 입력 가능하도록 추가

# ✅ 로그인 요청용
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ✅ 사용자 응답용 (기본 정보)
class UserResponse(BaseModel):
    user_id: str
    nickname: str
    is_active: bool
    role: str  # ✅ 관리자 여부 판별을 위한 필드
    is_admin: Optional[bool] = None  # ✅ 프론트에서 관리자 여부를 명시적으로 확인할 수 있도록 추가

    class Config:
        orm_mode = True

# ✅ 사용자 프로필 정보
class UserProfileSchema(BaseModel):
    email: EmailStr
    school: Optional[str] = None
    region: Optional[str] = None
    target_company: Optional[str] = None
    current_company: Optional[str] = None  # 선택 입력
    age: Optional[int] = None

    class Config:
        orm_mode = True
