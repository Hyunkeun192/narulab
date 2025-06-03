# backend/routers/user_reports.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from backend.database.database import get_db
# ✅ Report → UserReport로 이름 변경
from backend.models.response import UserReport
from backend.models.test import Test
from backend.schemas.report import ReportOut

router = APIRouter(
    prefix="/api/user",
    tags=["user-reports"]
)

# ✅ 사용자 ID 기준으로 리포트 목록 조회
@router.get("/reports/{user_id}", response_model=list[ReportOut])
def get_reports(user_id: UUID, db: Session = Depends(get_db)):
    reports = db.query(UserReport)  # ✅ Report → UserReport 이름 변경
    reports = reports.filter(UserReport.user_id == user_id).all()

    if not reports:
        raise HTTPException(status_code=404, detail="해당 사용자의 리포트가 없습니다.")

    return reports
