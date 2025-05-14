# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

# 회원가입 요청용
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str


# 사용자 응답용 (기본 정보)
class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    nickname: str
    is_active: bool

    class Config:
        orm_mode = True


# 사용자 프로필 정보
class UserProfileSchema(BaseModel):
    email: EmailStr
    school: Optional[str] = None
    region: Optional[str] = None
    target_company: Optional[str] = None
    current_company: Optional[str] = None
    age: Optional[int] = None

    class Config:
        orm_mode = True
