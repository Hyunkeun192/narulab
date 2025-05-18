from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/admin/ai-analysis",
    tags=["Admin - AI 분석 (Mock Only)"]
)

# 🔹 분석 요청용 Request Body 스키마
class AIAnalysisRequest(BaseModel):
    test_id: str

# 🔹 분석 결과 Response Body 스키마
class AIAnalysisSummary(BaseModel):
    test_id: str
    summary: str | None = None
    status: str  # 예: "not_ready", "ready"

# ✅ POST /api/admin/ai-analysis/analyze
@router.post("/analyze")
def analyze_test_with_ai(request: AIAnalysisRequest):
    """
    [Mock] 특정 검사에 대해 AI 분석을 시작합니다.
    실제 GPT 연동 없이 구조만 정의합니다.
    """
    return {
        "test_id": request.test_id,
        "status": "pending",
        "message": "AI 분석 기능은 추후 제공될 예정입니다."
    }

# ✅ GET /api/admin/ai-analysis/summary/{test_id}
@router.get("/summary/{test_id}", response_model=AIAnalysisSummary)
def get_ai_analysis_summary(test_id: str):
    """
    [Mock] 특정 검사에 대한 AI 분석 요약 결과 조회
    """
    return {
        "test_id": test_id,
        "summary": None,
        "status": "not_ready"
    }
