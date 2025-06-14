# backend/utils/init_db.py

from backend.database.database import Base, engine  # ✅ DB 연결을 위한 Base 클래스 및 engine 불러오기

# ✅ 모든 테이블 생성을 위해 필요한 모델들 import
# 주의: models/ 디렉토리 내 실제 존재하는 모든 모델을 정확히 import해야 create_all이 정상 작동함
from backend.models import (
    user,
    user_profile,
    user_deletion_log,
    institution_admin,
    report_rule,
    report_sten_distribution,
    response,
    notice,
    qna,
    test,
    questions,
    options,
    scoring_rules,
    test_question_links,
    test_analytics_by_group,
    question_stats_by_group,
    notifications,
    verification_code,
)

from backend.core.config import settings  # ✅ .env 환경설정에서 DATABASE_URL 불러오기

# ✅ 현재 로드된 데이터베이스 URL 출력 (디버깅용)
print(f"\n✅ Loaded DATABASE_URL: {settings.DATABASE_URL}")

# ✅ 모든 테이블 생성 시도
print("⏳ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created.")
