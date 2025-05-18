# routers/admin_group_analytics.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal, Optional
from database.database import get_db
from models.test_analytics_by_group import TestAnalyticsByGroup
from models.question_stats_by_group import QuestionStatsByGroup
from dependencies.admin_auth import get_current_admin_user  # ✅ 관리자 인증용

router = APIRouter(
    prefix="/api/analytics/groups",
    tags=["Admin - Group Analytics"],
    dependencies=[Depends(get_current_admin_user)]
)

# ✅ 그룹 통계 조회 API
@router.get("/")
def get_group_statistics(
    type: Literal["school", "region", "company", "age"] = Query(...),
    value: str = Query(...),
    year: Optional[int] = Query(None),    # ✅ 연도 필터 추가
    month: Optional[int] = Query(None),   # ✅ 월 필터 추가
    target: Literal["test", "question"] = Query("test"),  # 기본은 검사 단위
    db: Session = Depends(get_db)
):
    if target == "test":
        query = db.query(TestAnalyticsByGroup).filter(
            TestAnalyticsByGroup.group_type == type,
            TestAnalyticsByGroup.group_value == value
        )
        if year:
            query = query.filter(TestAnalyticsByGroup.year == year)  # ✅ 연도 조건 적용
        if month:
            query = query.filter(TestAnalyticsByGroup.month == month)  # ✅ 월 조건 적용
        stats = query.all()
    else:
        query = db.query(QuestionStatsByGroup).filter(
            QuestionStatsByGroup.group_type == type,
            QuestionStatsByGroup.group_value == value
        )
        if year:
            query = query.filter(QuestionStatsByGroup.year == year)  # ✅ 연도 조건 적용
        if month:
            query = query.filter(QuestionStatsByGroup.month == month)  # ✅ 월 조건 적용
        stats = query.all()

    return stats
