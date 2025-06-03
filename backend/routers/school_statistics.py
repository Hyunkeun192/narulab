# app/routers/school_statistics.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO
import pandas as pd

from backend.database.database import get_db
from backend.models.test import TestReport, Test  # ✅ Report 이름 중복 방지를 위해 수정
from backend.models.user import User
from backend.models.institution_admin import InstitutionAdmin
from backend.dependencies.external_admin_auth import get_school_admin_user
from backend.utils.encryption import aes_decrypt  # ✅ 이메일 복호화를 위해 추가됨

router = APIRouter(
    prefix="/api/school/statistics",
    tags=["School - Statistics"],
    dependencies=[Depends(get_school_admin_user)]  # ✅ 학교 관리자 전용 인증
)

# ✅ 소속 학교 학생들의 검사 결과 다운로드
@router.get("/reports/download")
def download_school_user_reports(
    current_admin: InstitutionAdmin = Depends(get_school_admin_user),
    db: Session = Depends(get_db)
):
    # ✅ 학교 관리자 정보 기준
    school_name = current_admin.institution_name

    # ✅ 소속 학교 학생 조회
    users = db.query(User).join(User.profile).filter(
        User.profile.has(school=school_name),
        User.is_active == True
    ).all()

    user_emails = [u.encrypted_email for u in users]  # ✅ 사용자 email 기준 필터링용

    reports = db.query(TestReport).filter(TestReport.email.in_(user_emails)).all()  # ✅ Report → TestReport
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
            "user_id": next((u.user_id for u in users if u.encrypted_email == r.email), "unknown"),
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
        headers={"Content-Disposition": "attachment; filename=school_reports.csv"}
    )

# ✅ 본교 vs 지역 vs 전체 평균 비교 API
@router.get("/compare")
def compare_school_statistics(
    test_id: str,
    db: Session = Depends(get_db),
    current_admin: InstitutionAdmin = Depends(get_school_admin_user)
):
    school_name = current_admin.institution_name

    school_users = db.query(User).join(User.profile).filter(
        User.profile.has(school=school_name)
    ).all()
    school_ids = [u.user_id for u in school_users]

    region = school_users[0].profile.region if school_users else None
    region_users = db.query(User).join(User.profile).filter(
        User.profile.has(region=region)
    ).all() if region else []

    all_users = db.query(User).all()

    # ✅ 리포트 가져오기 함수: Report → TestReport
    def get_scores(user_list):
        uids = [u.user_id for u in user_list]
        reports = db.query(TestReport).filter(
            TestReport.test_id == test_id,
            TestReport.user_id.in_(uids)
        ).all()
        return [r.score_total for r in reports]

    school_scores = get_scores(school_users)
    region_scores = get_scores(region_users)
    all_scores = get_scores(all_users)

    def calc_stats(scores):
        return {
            "avg_score": round(sum(scores)/len(scores), 2) if scores else None,
            "user_count": len(scores)
        }

    return {
        "test_id": test_id,
        "school": {"name": school_name, **calc_stats(school_scores)},
        "region": {"name": region, **calc_stats(region_scores)},
        "all": {"name": "전체", **calc_stats(all_scores)}
    }
