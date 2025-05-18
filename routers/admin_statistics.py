from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID
from io import StringIO
from typing import Optional, Any
import pandas as pd

from database.database import get_db
from models.test import Report, Test
from models.user import User
from dependencies.admin_auth import get_super_admin_user
from schemas.test_analytics import (
    TestAnalyticsSummary,
    TestAnalyticsDetail,
    QuestionAnalytics,
    ResponseAnalyticsSummary,
    GroupAnalyticsSummary
)

# ✅ 관리자 통계 조회 라우터
router = APIRouter(
    prefix="/api/admin/statistics",
    tags=["Admin - Statistics"],
    dependencies=[Depends(get_super_admin_user)]  # ✅ 슈퍼 관리자 인증
)

# ✅ 전체 검사별 통계 요약
@router.get("/tests", response_model=list[TestAnalyticsSummary])
def get_all_test_stats(db: Session = Depends(get_db)):
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

# ✅ 응답 기반 필터 통계
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

# ✅ 그룹별 통계 비교
@router.get("/groups", response_model=GroupAnalyticsSummary)
def get_group_stats(
    type: str = Query(...),
    value: str = Query(...),
    db: Session = Depends(get_db)
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

# ✅ 사용자 + 리포트 데이터 다운로드 (CSV)
@router.get("/download")
def download_user_reports(db: Session = Depends(get_db)):
    users = db.query(User).all()
    reports = db.query(Report).all()
    tests = {t.test_id: t.test_name for t in db.query(Test).all()}

    # 사용자 DF
    user_df = pd.DataFrame([
        {
            "user_id": u.user_id,
            "nickname": u.nickname,
            "subscription": u.subscription,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ])

    # 리포트 DF (검사별 점수 & 생성일)
    report_rows = []
    for r in reports:
        report_rows.append({
            "user_id": r.user_id,
            f"{tests.get(r.test_id, 'Unknown')}_score": r.score_total,
            f"{tests.get(r.test_id, 'Unknown')}_date": r.report_generated_at.strftime("%Y-%m-%d")
        })
    report_df = pd.DataFrame(report_rows)

    # 검사별 열 확장 (pivot-like merge)
    final_df = user_df.copy()
    if not report_df.empty:
        report_wide = report_df.groupby("user_id").first().reset_index()
        final_df = pd.merge(user_df, report_wide, on="user_id", how="left")

    # CSV 스트리밍
    buffer = StringIO()
    final_df.to_csv(buffer, index=False)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=all_user_reports.csv"}
    )

# ✅ 특정 검사 결과 다운로드 (CSV)
@router.get("/tests/{test_id}/download")
def download_specific_test_results(test_id: UUID, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="검사를 찾을 수 없습니다.")

    reports = db.query(Report).filter(Report.test_id == test_id).all()
    if not reports:
        raise HTTPException(status_code=404, detail="해당 검사에 대한 결과가 없습니다.")

    user_map = {
        u.user_id: u.nickname for u in db.query(User).all()
    }

    data = []
    for r in reports:
        data.append({
            "user_id": r.user_id,
            "nickname": user_map.get(r.user_id, "Unknown"),
            "score_total": r.score_total,
            "report_generated_at": r.report_generated_at.strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(data)
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    filename = f"{test.test_name}_결과.csv"

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ✅ 학교/지역/학과 기반 평균 비교 API
@router.get("/compare")
def compare_group_scores(
    test_id: UUID,
    filter_school: Optional[str] = Query(None),
    compare_school: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    group_by: Optional[str] = Query("school"),  # school / region / department
    db: Session = Depends(get_db)
):
    # 검사 존재 확인
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="검사를 찾을 수 없습니다.")

    # 리포트 + 사용자 정보 조인
    query = (
        db.query(User, Report)
        .join(Report, User.user_id == Report.user_id)
        .filter(Report.test_id == test_id)
    )

    # 조건 필터 적용
    if filter_school:
        query = query.filter(User.profile.has(school=filter_school))
    if region:
        query = query.filter(User.profile.has(region=region))
    if department:
        query = query.filter(User.profile.has(department=department))
    if compare_school:
        query = query.union_all(
            db.query(User, Report)
            .join(Report, User.user_id == Report.user_id)
            .filter(Report.test_id == test_id)
            .filter(User.profile.has(school=compare_school))
        )

    # 결과 수집
    records = query.all()
    data = []
    for user, report in records:
        group_key = None
        if group_by == "school":
            group_key = user.profile.school
        elif group_by == "region":
            group_key = user.profile.region
        elif group_by == "department":
            group_key = user.profile.target_company or "전체"
        else:
            group_key = "기타"

        data.append({
            "group": group_key,
            "score": report.score_total
        })

    # 그룹 평균 계산
    df = pd.DataFrame(data)
    if df.empty:
        return {"test_name": test.test_name, "groups": []}

    summary = (
        df.groupby("group")["score"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "avg_score", "count": "user_count"})
    )

    return {
        "test_name": test.test_name,
        "groups": summary.to_dict(orient="records")
    }

@router.get("/summary")
def get_system_statistics_summary(db: Session = Depends(get_db)):
    """
    전체 사용자 / 테스트 / 리포트 수 등 요약 정보 반환
    """
    total_users = db.query(User).count()
    total_tests = db.query(Test).count()
    total_reports = db.query(Report).count()

    avg_score = db.query(Report.score_total).all()
    scores = [r[0] for r in avg_score if r[0] is not None]
    average_score = sum(scores) / len(scores) if scores else None

    return {
        "total_users": total_users,
        "total_tests": total_tests,
        "total_reports": total_reports,
        "average_score": average_score
    }

@router.get("/tests/{test_id}/results")
def get_test_result_summary(test_id: UUID, db: Session = Depends(get_db)):
    """
    특정 테스트 결과 평균, 최고/최저, STEN 분포
    """
    reports = db.query(Report).filter(Report.test_id == test_id).all()
    scores = [r.score_total for r in reports if r.score_total is not None]

    sten_distribution = {}
    for i in range(1, 10):
        sten_distribution[f"STEN {i}"] = sum(1 for r in reports if r.score_level == f"STEN {i}")

    return {
        "test_id": test_id,
        "average_score": round(sum(scores) / len(scores), 2) if scores else None,
        "min_score": min(scores) if scores else None,
        "max_score": max(scores) if scores else None,
        "sten_distribution": sten_distribution
    }

