from database.database import Base, engine

# ✅ 각 모델 안의 실제 클래스 import
from models.user import User
from models.question import Question, QuestionStatus
from models.test import Test
from models.option import Option
from models.notification import Notification
from models.institution_admin import InstitutionAdmin
from models.verification_code import VerificationCode  # ✅ 추가된 인증 모델
from models.user_deletion_log import UserDeletionLog  # ✅ 사용자 탈퇴 로그 모델 추가
from models.test_analytics_by_group import TestAnalyticsByGroup
from models.question_stats_by_group import QuestionStatsByGroup

import models  # ✅ __init__.py에서 모든 모델 import되어 있어야 함

print("📦 Creating all tables in the database...")
Base.metadata.create_all(bind=engine)
print("✅ Table creation completed.")
