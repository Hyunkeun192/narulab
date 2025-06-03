from backend.database.database import Base, engine

# ✅ 모델들 import
from backend.models.user import User
from backend.models.question import Question, QuestionStatus
from backend.models.test import Test, TestReport  # ✅ TestReport 명시적 import
from backend.models.option import Option
from backend.models.notification import Notification
from backend.models.institution_admin import InstitutionAdmin
from backend.models.verification_code import VerificationCode
from backend.models.user_deletion_log import UserDeletionLog
from backend.models.test_analytics_by_group import TestAnalyticsByGroup
from backend.models.question_stats_by_group import QuestionStatsByGroup
from backend.models.notice import Notice
from backend.models.qna import QnA
from backend.models.response import UserReport  # ✅ UserReport 명시적 import

from backend import models

print("📦 Creating all tables in the database...")
Base.metadata.create_all(bind=engine)
print("✅ Table creation completed.")
