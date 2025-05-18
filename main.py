# main.py

import os
print("[DEBUG] main.py 실행 위치:", os.path.abspath(__file__))

import builtins
import typing
builtins.Any = typing.Any  # ✅ 모든 eval(), 모든 서브모듈, 모든 프로세스에서 유효

from fastapi import FastAPI

# ✅ 라우터 import
from routers import user, tests, reports, notifications, subscribe, ai
from routers import admin_tests
from routers import admin_questions
from routers import admin_statistics
from routers import admin_ai_review       # ✅ 추가됨: AI 분석 라우터
from routers import admin_analytics       # ✅ 추가됨: 관리자 대시보드 통계
from routers import admin_scoring_rules   # ✅ 추가됨: 채점 기준 설정 라우터
from routers import school_statistics, company_statistics
from routers import admin_external_admins
from routers import verification
from routers import admin_users
from routers import admin_ai_analysis
from routers import admin_group_analytics  # ✅ 추가

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
app.include_router(admin_questions.router)       # ✅ 관리자 문항 라우터 등록
app.include_router(admin_statistics.router)      # ✅ 슈퍼 관리자 통계 다운로드 등록
app.include_router(admin_tests.router)           # ✅ 관리자 테스트 라우터 등록
app.include_router(admin_ai_review.router)       # ✅ 추가됨
app.include_router(admin_analytics.router)       # ✅ 추가됨
app.include_router(admin_scoring_rules.router)   # ✅ 추가됨
app.include_router(school_statistics.router)     # ✅ 학교 관리자 라우터
app.include_router(company_statistics.router)    # ✅ 기업 관리자 라우터
app.include_router(admin_external_admins.router)
app.include_router(verification.router)
app.include_router(admin_users.router)
app.include_router(admin_ai_analysis.router)
app.include_router(admin_group_analytics.router)

# ✅ 루트 경로 확인용
@app.get("/")
def read_root():
    return {"message": "Welcome to Narulab API!"}

if __name__ == "__main__":
    from database.database import Base, engine
    Base.metadata.create_all(bind=engine)
