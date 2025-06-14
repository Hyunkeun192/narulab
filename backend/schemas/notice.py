# backend/schemas/notice.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ✅ 공지사항 생성 요청 스키마
class NoticeCreate(BaseModel):
    title: str  # 제목
    content: str  # 내용

# ✅ 공지사항 수정 요청 스키마
class NoticeUpdate(BaseModel):
    title: Optional[str] = None  # 수정할 제목 (선택)
    content: Optional[str] = None  # 수정할 내용 (선택)

# ✅ 공지사항 조회 응답 스키마
class NoticeOut(BaseModel):
    id: str  # 공지 ID (UUID 문자열)
    title: str  # 제목
    content: str  # 내용
    created_at: datetime  # 생성일시
    updated_at: Optional[datetime] = None  # 수정일시
    creator_id: str  # 작성자 ID

    class Config:
        orm_mode = True  # ✅ ORM 객체를 그대로 받아도 Pydantic이 변환 가능하게 함
