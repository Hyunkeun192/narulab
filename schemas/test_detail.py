from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from models.question import QuestionStatus

# 🔸 선택지 출력용 스키마
class OptionItem(BaseModel):
    option_id: UUID                      # 선택지 ID
    option_text: str                     # 선택지 텍스트
    is_correct: bool                     # 정답 여부
    option_image_url: Optional[str] = None  # 선택지 이미지 URL (선택)
    option_order: int                    # 보기 순서

    class Config:
        orm_mode = True

# 🔸 문항 + 선택지 스키마
class QuestionWithOptions(BaseModel):
    question_id: UUID
    question_text: str
    question_type: str
    is_multiple_choice: bool
    status: QuestionStatus
    options: List[OptionItem]            # 하위 선택지 목록

    class Config:
        orm_mode = True

# 🔸 검사 상세 구성 응답 스키마
class TestDetailResponse(BaseModel):
    test_id: UUID
    test_name: str
    test_type: str
    version: str
    duration_minutes: int
    questions: List[QuestionWithOptions]  # 연결된 문항 목록

    class Config:
        orm_mode = True
