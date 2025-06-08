from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from backend.models.question import QuestionStatus

# 🔸 옵션 스키마 추가
class OptionItem(BaseModel):
    option_text: str
    is_correct: bool

    class Config:
        orm_mode = True

# 🔸 문항 목록 출력용 스키마
class QuestionListItem(BaseModel):
    question_id: UUID
    test_id: Optional[UUID] = None
    question_text: str
    question_type: str
    is_multiple_choice: bool
    status: QuestionStatus
    created_at: datetime
    question_name: Optional[str] = None
    instruction: Optional[str] = None
    correct_explanation: Optional[str] = None
    wrong_explanation: Optional[str] = None

    # ✅ 옵션 필드 추가
    options: List[OptionItem] = []

    class Config:
        orm_mode = True
