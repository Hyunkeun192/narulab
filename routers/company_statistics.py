# app/routers/company_statistics.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO
import pandas as pd

from app.database import get_db
from app.models.test import Report, Test
from app.models.user import User
from app.models.institution_admin import InstitutionAdmin
from app.dependencies.external_admin_auth import get_company_admin_user

router = APIRouter(
    prefix="/api/company/statistics",
    tags=["Company - Statistics"],
    dependencies=[Depends(get_company_admin_user)]  # ✅ 기업 관리자 전용 인증
)

# ✅ 소속 기업 지원자 검사 결과 다운로드
@router.get("/reports/download")
def download_company_user_reports(
    current_admin: InstitutionAdmin = Depends(get_company_admin_user),
    db: Session = Depends(get_db)
):
    company = current_admin.institution_name

    users = db.query(User).join(User.profile).filter(
        User.profile.has(current_company=company),
        User.is_active == True
    ).all()

    user_ids = [u.user_id for u in users]
    reports = db.query(Report).filter(Report.user_id.in_(user_ids)).all()
    tests = {t.test_id: t.test_name for t in db.query(Test).all()}

    user_df = pd.DataFrame([
        {
            "user_id": u.user_id,
            "nickname": u.nickname,
            "subscription": u.subscription,
            "created_at": u.created_at
        }
        for u in users
    ])

    report_rows = []
    for r in reports:
        report_rows.append({
            "user_id": r.user_id,
            f"{tests.get(r.test_id, 'Unknown')}_score": r.score_total,
            f"{tests.get(r.test_id, 'Unknown')}_date": r.report_generated_at.strftime("%Y-%m-%d")
        })
    report_df = pd.DataFrame(report_rows)

    final_df = user_df.copy()
    if not report_df.empty:
        report_wide = report_df.groupby("user_id").first().reset_index()
        final_df = pd.merge(user_df, report_wide, on="user_id", how="left")

    buffer = StringIO()
    final_df.to_csv(buffer, index=False)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={company}_지원자결과.csv"}
    )

# ✅ 기업 지원자 vs 전체 평균 비교
@router.get("/compare")
def compare_company_statistics(
    test_id: str,
    db: Session = Depends(get_db),
    current_admin: InstitutionAdmin = Depends(get_company_admin_user)
):
    company = current_admin.institution_name

    company_users = db.query(User).join(User.profile).filter(
        User.profile.has(current_company=company)
    ).all()
    all_users = db.query(User).all()

    def get_scores(user_list):
        uids = [u.user_id for u in user_list]
        reports = db.query(Report).filter(
            Report.test_id == test_id,
            Report.user_id.in_(uids)
        ).all()
        return [r.score_total for r in reports]

    company_scores = get_scores(company_users)
    all_scores = get_scores(all_users)

    def calc_stats(scores):
        return {
            "avg_score": round(sum(scores)/len(scores), 2) if scores else None,
            "user_count": len(scores)
        }

    return {
        "test_id": test_id,
        "company": {"name": company, **calc_stats(company_scores)},
        "all": {"name": "전체", **calc_stats(all_scores)}
    }
