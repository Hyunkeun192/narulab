# app/routers/ai.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List, Any

router = APIRouter()


# ✅ 리포트 요약 요청/응답 스키마
class SummaryRequest(BaseModel):
    score_profile: Dict[str, int]
    target_company: str

class SummaryResponse(BaseModel):
    summary: str


# ✅ GPT 기반 리포트 요약 생성 API
@router.post("/api/ai/summary", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest):
    summary_text = f"{request.target_company}와의 적합도를 기반으로, " \
                   f"{', '.join(request.score_profile.keys())} 영역에서 우수한 성과를 보였습니다."
    return SummaryResponse(summary=summary_text)


# ✅ GPT 문항 생성 요청/응답 스키마
class QuestionGenRequest(BaseModel):
    topic: str            # 예: "논리 추론"
    difficulty: str       # 예: "중"
    question_type: str    # 예: "text"
    num_options: int      # 보기 개수

class OptionOut(BaseModel):
    option_text: str
    is_correct: bool

class QuestionGenResponse(BaseModel):
    question_text: str
    options: List[OptionOut]
    explanation: str


# ✅ GPT 기반 문항 생성 API
@router.post("/api/ai/generate-question", response_model=QuestionGenResponse)
def generate_question(request: QuestionGenRequest):
    # TODO: GPT 연동 시 OpenAI API 호출 처리 예정

    # 임시 더미 데이터 생성
    options = [
        OptionOut(option_text="선택지 A", is_correct=True),
        OptionOut(option_text="선택지 B", is_correct=False),
        OptionOut(option_text="선택지 C", is_correct=False),
        OptionOut(option_text="선택지 D", is_correct=False),
    ]

    return QuestionGenResponse(
        question_text=f"[{request.topic}] 관련된 문제입니다. 가장 알맞은 답을 고르세요.",
        options=options[:request.num_options],
        explanation="정답은 선택지 A입니다. 이유는 예시입니다."
    )
