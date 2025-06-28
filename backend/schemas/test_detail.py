from pydantic import BaseModel
from typing import List, Optional, Any
from uuid import UUID
from backend.models.question import QuestionStatus

# 🔸 선택지 출력용 스키마
class OptionItem(BaseModel):
    option_id: UUID                      # 선택지 ID
    option_text: str                     # 선택지 텍스트
    is_correct: bool                     # 정답 여부
    option_image_url: Optional[str] = None  # 선택지 이미지 URL (선택)
    option_order: int                    # 보기 순서

    class Config:
        model_config = {
        "from_attributes": True
    }

# 🔸 문항 + 선택지 스키마
class QuestionWithOptions(BaseModel):
    question_id: UUID
    question_text: str
    question_type: str
    is_multiple_choice: bool
    status: QuestionStatus
    options: List[OptionItem]            # 하위 선택지 목록

    class Config:
        model_config = {
        "from_attributes": True
    }

# 🔸 검사 상세 구성 응답 스키마
class TestDetailResponse(BaseModel):
    test_id: UUID
    test_name: str
    test_type: str
    version: str
    duration_minutes: int
    questions: List[QuestionWithOptions]  # 연결된 문항 목록

    class Config:
        model_config = {
        "from_attributes": True
    }

# 🔹 보기 모델 (옵션)
class OptionOut(BaseModel):
    option_id: str
    option_text: str
    is_correct: Optional[bool] = False

    class Config:
        orm_mode = True

# 🔹 문항 + 보기 포함 모델
class QuestionWithOptionsOut(BaseModel):
    question_id: str
    question_name: Optional[str]
    instruction: Optional[str]
    question_text: Optional[str]
    options: List[OptionOut] = []

    class Config:
        orm_mode = True

class QuestionIdList(BaseModel):
    question_ids: List[str]

class TestSummary(BaseModel):
    test_id: str
    test_name: str
    test_type: str
    is_published: bool
    question_count: Optional[int]  # ✅ 이 필드가 핵심!

# ✅ 검사 생성 요청 모델 정의
class TestCreateRequest(BaseModel):
    test_name: str                     # 검사명
    test_type: str                     # 검사 유형 (예: aptitude, personality)
    version: str                       # 버전명 (예: v1.0)
    duration_minutes: int             # ✅ 소요 시간(분) — 프론트에서 입력받은 값
