# backend/utils/init_db.py

from backend.database.database import Base, engine  # ✅ DB 연결을 위한 Base 클래스 및 engine 불러오기
from backend.core.config import settings  # ✅ .env 환경설정에서 DATABASE_URL 불러오기

# ✅ 모든 테이블 생성을 위해 필요한 모델들 import
# 주의: models/ 디렉토리 내 실제 존재하는 모든 모델을 정확히 import해야 create_all이 정상 작동함
from backend.models import (
    User, UserProfile, UserDeletionLog,         # ✅ user.py
    InstitutionAdmin,                           # ✅ institution_admin.py
    ReportRule, ReportSTENDistribution,         # ✅ report_rule.py, report_sten_distribution.py
    UserTestHistory,                                  # ✅ response.py
    Notice, QnA,                                 # ✅ notice.py, qna.py
    Test,                                        # ✅ test.py
    Question, QuestionStatsByGroup,             # ✅ question.py, question_stats_by_group.py
    Option,                                      # ✅ option.py
    ScoringRule,                                 # ✅ scoring_rule.py
    TestQuestionLink,                            # ✅ test_question_links.py
    TestAnalyticsByGroup,                        # ✅ test_analytics_by_group.py
    Notification,                                # ✅ notification.py
    VerificationCode,                            # ✅ verification_code.py
    NormGroup                                    # ✅ norm_group.py
)

# ✅ 현재 로드된 데이터베이스 URL 출력 (디버깅용)
print(f"\n✅ Loaded DATABASE_URL: {settings.DATABASE_URL}")

# ✅ 모든 테이블 생성 시도
print("⏳ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created.")
