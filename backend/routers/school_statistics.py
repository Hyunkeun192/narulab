# app/routers/school_statistics.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO
import pandas as pd

from backend.database.database import get_db
from backend.models.test import Report, Test
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

    # ✅ 기존 user_id → Report.user_id ❌ 오류 → Report.email로 수정 필요
    user_emails = [u.encrypted_email for u in users]  # ✅ 사용자 email 기준 필터링용

    reports = db.query(Report).filter(Report.email.in_(user_emails)).all()  # ✅ 수정: Report.user_id → Report.email
    tests = {t.test_id: t.test_name for t in db.query(Test).all()}

    # ✅ 사용자 DF
    user_df = pd.DataFrame([
        {
            "user_id": u.user_id,
            "nickname": u.nickname,
            "subscription": u.subscription,
            "created_at": u.created_at
        }
        for u in users
    ])

    # ✅ 리포트 DF
    report_rows = []
    for r in reports:
        report_rows.append({
            "user_id": next((u.user_id for u in users if u.encrypted_email == r.email), "unknown"),  # ✅ 매칭된 user_id 역추적
            f"{tests.get(r.test_id, 'Unknown')}_score": r.score_total,
            f"{tests.get(r.test_id, 'Unknown')}_date": r.report_generated_at.strftime("%Y-%m-%d")
        })
    report_df = pd.DataFrame(report_rows)

    # ✅ 열 병합
    final_df = user_df.copy()
    if not report_df.empty:
        report_wide = report_df.groupby("user_id").first().reset_index()
        final_df = pd.merge(user_df, report_wide, on="user_id", how="left")

    buffer = StringIO()
    final_df.to_csv(buffer, index=False)
    buffer.seek(0)

    # ✅ 수정: 한글 포함된 파일명 제거 → latin-1 인코딩 오류 방지
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

    # ✅ 소속 학교 사용자 조회
    school_users = db.query(User).join(User.profile).filter(
        User.profile.has(school=school_name)
    ).all()
    school_ids = [u.user_id for u in school_users]

    # ✅ 지역 기준 (학교 관리자 등록된 지역을 기준으로 잡음)
    region = school_users[0].profile.region if school_users else None
    region_users = db.query(User).join(User.profile).filter(
        User.profile.has(region=region)
    ).all() if region else []

    # ✅ 전체 사용자 조회
    all_users = db.query(User).all()

    # ✅ 리포트 가져오기
    def get_scores(user_list):
        uids = [u.user_id for u in user_list]
        reports = db.query(Report).filter(
            Report.test_id == test_id,
            Report.user_id.in_(uids)
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
