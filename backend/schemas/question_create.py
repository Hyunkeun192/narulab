from pydantic import BaseModel
from typing import List, Optional, Any
from uuid import UUID

# 🔸 선택지 요청 스키마
class OptionItem(BaseModel):
    option_text: str                     # 보기 텍스트
    is_correct: bool                     # 정답 여부 (객관식일 경우)
    option_image_url: Optional[str] = None  # 이미지 선택지 (선택)

# 🔸 문항 생성 요청 스키마
class QuestionCreateRequest(BaseModel):
    test_id: UUID
    question_text: str
    question_type: str                   # text / image 등
    is_multiple_choice: bool
    options: List[OptionItem]

# 🔸 문항 생성 응답 스키마
class QuestionCreateResponse(BaseModel):
    question_id: UUID
    message: str
