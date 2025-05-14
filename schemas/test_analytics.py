from pydantic import BaseModel
from typing import List, Dict, Optional
from uuid import UUID

# 🔸 전체 검사별 요약 통계
class TestAnalyticsSummary(BaseModel):
    test_id: UUID
    test_name: str
    num_participants: int
    avg_total_score: float
    std_total_score: float
    completion_rate: float

# 🔸 특정 검사 상세 통계
class TestAnalyticsDetail(BaseModel):
    test_id: UUID
    avg_duration_minutes: float
    overall_correct_rate: float
    score_distribution: Dict[str, int]  # 예: {"70-80": 12, "80-90": 33}

# 🔸 문항별 통계
class QuestionAnalytics(BaseModel):
    question_id: UUID
    num_responses: int
    correct_rate: float
    avg_response_time: float
    option_distribution: Dict[str, float]  # 예: {"opt-a": 45.3, "opt-b": 30.2}

# 🔸 응답 기반 필터 통계
class ResponseAnalyticsSummary(BaseModel):
    total_users: int
    avg_score: float
    dominant_level: str
    top_3_schools: List[str]

# 🔸 그룹별 비교 통계
class GroupAnalyticsSummary(BaseModel):
    group: str
    avg_score: float
    dominant_score_level: str
    score_distribution: Dict[str, int]  # 예: {"STEN 6~7": 28, "STEN 8 이상": 14}
