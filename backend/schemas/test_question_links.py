# backend/schemas/test_question_links.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ✅ 문항 연결용 요청 스키마
class TestQuestionLinkCreate(BaseModel):
    test_id: str                         # 검사 ID
    question_id: str                     # 연결할 문항 ID
    order_index: Optional[int] = None    # (선택) 문항 순서

# ✅ 응답용 스키마
class TestQuestionLinkOut(BaseModel):
    id: str
    test_id: str
    question_id: str
    order_index: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ SQLAlchemy 연동을 위한 설정
