from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Any

from database.database import get_db
from schemas.test_analytics import (
    TestAnalyticsSummary,
    TestAnalyticsDetail,
    QuestionAnalytics,
    ResponseAnalyticsSummary,
    GroupAnalyticsSummary
)

# ✅ 관리자 인증 의존성 import
from dependencies.admin_auth import get_current_admin_user

# 관리자 통계 조회 라우터
router = APIRouter(
    prefix="/api/analytics",
    tags=["Admin - Analytics"],
    dependencies=[Depends(get_current_admin_user)]  # ✅ 관리자 인증 적용
)

# ✅ 전체 검사별 통계 요약
@router.get("/tests", response_model=List[TestAnalyticsSummary])
def get_all_test_stats(db: Session = Depends(get_db)):
    # ✅ 예시 데이터 — 실제 구현 시 DB 분석 로직 필요
    return [
        TestAnalyticsSummary(
            test_id=UUID("11111111-1111-1111-1111-111111111111"),
            test_name="종합 적성 검사 A형",
            num_participants=234,
            avg_total_score=78.4,
            std_total_score=9.2,
            completion_rate=0.95
        )
    ]

# ✅ 특정 검사 상세 통계
@router.get("/tests/{test_id}", response_model=TestAnalyticsDetail)
def get_test_detail_stats(test_id: UUID, db: Session = Depends(get_db)):
    return TestAnalyticsDetail(
        test_id=test_id,
        avg_duration_minutes=25.3,
        overall_correct_rate=0.82,
        score_distribution={
            "60-70": 21,
            "70-80": 55,
            "80-90": 38
        }
    )

# ✅ 문항별 통계
@router.get("/questions/{question_id}", response_model=QuestionAnalytics)
def get_question_stats(question_id: UUID, db: Session = Depends(get_db)):
    return QuestionAnalytics(
        question_id=question_id,
        num_responses=1410,
        correct_rate=0.64,
        avg_response_time=8.2,
        option_distribution={
            "opt-a": 45.2,
            "opt-b": 33.1,
            "opt-c": 15.0,
            "opt-d": 6.7
        }
    )

# ✅ 응답 기반 필터 통계 (예: 학교 필터)
@router.get("/responses", response_model=ResponseAnalyticsSummary)
def get_response_stats(
    filter: str = Query(None),
    db: Session = Depends(get_db)
):
    return ResponseAnalyticsSummary(
        total_users=202,
        avg_score=75.6,
        dominant_level="STEN 6",
        top_3_schools=["서울대", "연세대", "고려대"]
    )

# ✅ 그룹별 통계 비교 (학교/지역/기업 등)
@router.get("/groups", response_model=GroupAnalyticsSummary)
def get_group_stats(
    type: str = Query(...), value: str = Query(...), db: Session = Depends(get_db)
):
    if type not in ["school", "region", "company", "age"]:
        raise HTTPException(status_code=400, detail="Invalid group type")

    return GroupAnalyticsSummary(
        group=value,
        avg_score=81.2,
        dominant_score_level="STEN 7",
        score_distribution={
            "STEN 6 이하": 10,
            "STEN 7~8": 22,
            "STEN 9~10": 8
        }
    )

