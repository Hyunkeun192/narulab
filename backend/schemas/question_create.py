from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from enum import Enum  # 🔸 Enum 추가

# 🔸 usage_type enum 정의
class UsageType(str, Enum):
    aptitude = "aptitude"
    personality = "personality"

# 🔸 선택지 요청 스키마
class OptionItem(BaseModel):
    option_text: str
    is_correct: bool
    option_order: Optional[int] = None
    option_image_url: Optional[str] = None
    option_id: Optional[UUID] = None

# 🔸 문항 생성 요청 스키마
class QuestionCreateRequest(BaseModel):
    test_id: Optional[UUID] = None                # ✅ 필수 → 선택으로 변경
    question_name: Optional[str] = None           # ✅ 프론트엔드 전송값 수용
    question_text: str                            # 문항 질문 텍스트
    question_type: str                            # text / image 등
    is_multiple_choice: bool
    options: List[OptionItem]

    # ✅ 추가: 적성/인성 구분
    usage_type: UsageType                         # 🔸 aptitude / personality

    # ✅ 지시문 (지문)
    instruction: Optional[str] = None             # 예: "다음을 읽고 물음에 답하시오"

    # ✅ 정답/오답 해설 (피드백 제공용)
    correct_explanation: Optional[str] = None     # 정답 해설
    wrong_explanation: Optional[str] = None       # 오답 해설

    # ✅ 이미지 기반 문항인 경우
    question_image_url: Optional[str] = None      # 문항 이미지 URL

# 🔸 문항 생성 응답 스키마
class QuestionCreateResponse(BaseModel):
    question_id: UUID
    message: str
