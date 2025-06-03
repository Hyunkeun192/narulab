# backend/routers/admin_pdf.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID
from backend.database.database import get_db
# ✅ Report → UserReport로 클래스명 변경
from backend.models.response import UserReport
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import tempfile

router = APIRouter(
    prefix="/api/admin/reports",
    tags=["admin-pdf"]
)

# ✅ 리포트 PDF 다운로드 (학교/기업 관리자 전용)
@router.get("/pdf/{report_id}")
def download_report_pdf(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(UserReport).filter(UserReport.report_id == report_id).first()  # ✅ Report → UserReport 이름 변경

    if not report:
        raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")

    # ✅ HTML 템플릿 렌더링 (Jinja2)
    env = Environment(loader=FileSystemLoader("backend/templates"))
    template = env.get_template("report_template.html")

    html_out = template.render(
        report_id=report.report_id,
        score=report.score,
        sten=report.sten,
        description=report.description,
        created_at=report.created_at,
    )

    # ✅ 임시 PDF 파일 생성
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    HTML(string=html_out).write_pdf(tmp_pdf.name)

    return FileResponse(
        path=tmp_pdf.name,
        filename=f"report_{report.report_id}.pdf",
        media_type="application/pdf"
    )
