# app/routers/reports.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.test import Report, Test
from typing import List
from pydantic import BaseModel
from datetime import datetime

# ✅ PDF 다운로드 관련 추가 import
from fastapi.responses import Response
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

router = APIRouter()


# ✅ DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ 리포트 요약 응답 스키마
class ReportSummary(BaseModel):
    report_id: str
    test_id: str
    test_name: str
    score_total: float
    score_level: str
    report_generated_at: datetime

    class Config:
        orm_mode = True


# ✅ 리포트 상세 응답 스키마
class ReportDetail(BaseModel):
    report_id: str
    test_name: str
    score_total: float
    score_standardized: float
    score_level: str
    result_summary: str

    class Config:
        orm_mode = True


# ✅ 리포트 목록 조회 API
@router.get("/api/reports/me", response_model=List[ReportSummary])
def get_my_reports(email: str, db: Session = Depends(get_db)):
    # 암호화된 이메일 기준 조회
    reports = db.query(Report).filter(Report.email == email).order_by(Report.report_generated_at.desc()).all()

    # 각 리포트에 검사명 포함
    result = []
    for r in reports:
        test = db.query(Test).filter(Test.test_id == r.test_id).first()
        result.append(ReportSummary(
            report_id=r.report_id,
            test_id=r.test_id,
            test_name=test.test_name if test else "Unknown",
            score_total=r.score_total,
            score_level=r.score_level,
            report_generated_at=r.report_generated_at
        ))
    return result


# ✅ 리포트 상세 조회 API
@router.get("/api/reports/{report_id}", response_model=ReportDetail)
def get_report_detail(report_id: str, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    test = db.query(Test).filter(Test.test_id == report.test_id).first()

    return ReportDetail(
        report_id=report.report_id,
        test_name=test.test_name if test else "Unknown",
        score_total=report.score_total,
        score_standardized=report.score_standardized,
        score_level=report.score_level,
        result_summary=report.result_summary
    )


# ✅ 리포트 PDF 다운로드 API
@router.get("/api/reports/{report_id}/download/pdf")
def download_report_pdf(report_id: str, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    test = db.query(Test).filter(Test.test_id == report.test_id).first()
    test_name = test.test_name if test else "Unknown"

    # 템플릿 렌더링
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report_pdf.html")

    html_content = template.render(report={
        "test_name": test_name,
        "generated_at": report.report_generated_at.strftime("%Y-%m-%d"),
        "score_total": report.score_total,
        "score_level": report.score_level,
        "score_standardized": report.score_standardized,
        "result_summary": report.result_summary
    })

    # PDF 생성
    pdf = HTML(string=html_content).write_pdf()

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{report_id}.pdf"}
    )
