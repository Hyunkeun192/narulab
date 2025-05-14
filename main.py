# app/main.py

from fastapi import FastAPI
from app.routers import user, tests, reports, notifications, subscribe, ai  # ✅ 모든 라우터 import
from app.routers import admin_questions  # ✅ 관리자 문항 라우터 추가
from app.routers import admin_statistics  # ✅ 통계 다운로드 라우터 import 추가
from app.routers import school_statistics, company_statistics
from app.routers import admin_external_admins

app = FastAPI(
    title="Narulab API",
    description="취업 역량 진단 및 리포트 예측 플랫폼",
    version="1.0.0",
)

# ✅ 라우터 등록
app.include_router(user.router)
app.include_router(tests.router)
app.include_router(reports.router)
app.include_router(notifications.router)
app.include_router(subscribe.router)
app.include_router(ai.router)
app.include_router(admin_questions.router)  # ✅ 관리자 문항 라우터 등록
app.include_router(admin_statistics.router)  # ✅ 슈퍼 관리자 통계 다운로드 등록
app.include_router(school_statistics.router)   # ✅ 학교 관리자 라우터
app.include_router(company_statistics.router)  # ✅ 기업 관리자 라우터
app.include_router(admin_external_admins.router)

# ✅ 루트 경로 확인용
@app.get("/")
def read_root():
    return {"message": "Welcome to Narulab API!"}
