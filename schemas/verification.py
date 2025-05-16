# app/schemas/verification.py

from pydantic import BaseModel, EmailStr
from typing import Literal, Any

class VerificationRequest(BaseModel):
    type: Literal["email", "phone"]
    target: str  # 이메일 또는 전화번호

class VerificationConfirm(BaseModel):
    type: Literal["email", "phone"]
    target: str
    code: str
