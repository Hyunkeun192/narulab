from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID
from backend.models.question import QuestionStatus

# 🔸 AI 문항 목록 응답용 스키마
class AIQuestionListItem(BaseModel):
    question_id: UUID
    question_text: str
    question_type: str
    status: QuestionStatus

    class Config:
        model_config = {
        "from_attributes": True
    }

# 🔸 AI 문항 상세 조회 응답 스키마
class AIQuestionDetail(BaseModel):
    question_id: UUID
    question_text: str
    question_type: str
    is_multiple_choice: bool
    options: List[dict]               # 단순 처리: option_text, is_correct 등 포함 예상
    ai_explanation: Optional[str]     # GPT가 생성한 해설 (예정 필드)
    status: QuestionStatus
    review_comment: Optional[str]

    class Config:
        model_config = {
        "from_attributes": True
    }

# 🔸 승인/반려 요청
class AIReviewRequest(BaseModel):
    approved: bool
    review_comment: Optional[str] = None

# 🔸 승인/반려 응답
class AIReviewResponse(BaseModel):
    message: str
