# backend/schemas/response.py

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID  # ✅ 올바른 위치에서 UUID import

# ✅ 사용자 응답 항목 (문항 + 선택지)
class AnswerInput(BaseModel):
    question_id: UUID
    selected_option_ids: List[UUID]

# ✅ 전체 응답 제출 시 요청 본문
class ResponseSubmit(BaseModel):
    user_id: UUID
    test_id: UUID
    answers: List[AnswerInput]

# ✅ 서버 응답 형식 (점수, STEN, 해석 문구)
class ReportResult(BaseModel):
    score: int
    sten: int
    description: str
