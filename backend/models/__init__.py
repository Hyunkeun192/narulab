# backend/models/__init__.py

# ✅ 사용자 및 관련 정보
from .user import User, UserProfile
from .user_deletion_log import UserDeletionLog

# ✅ 관리자
from .institution_admin import InstitutionAdmin

# ✅ 공지, 알림
from .notice import Notice
from .notification import Notification

# ✅ 문항, 선택지
from .question import Question
from .question_stats_by_group import QuestionStatsByGroup
from .option import Option

# ✅ 검사, 검사-문항 연결
from .test import Test
from .test_question_links import TestQuestionLink

# ✅ 검사 결과 및 분석
from .response import UserTestHistory
from .report_rule import ReportRule
from .report_sten_distribution import ReportSTENDistribution
from .sten_rule import STENRule
from .scoring_rule import ScoringRule
from .test_analytics_by_group import TestAnalyticsByGroup
from .norm_group import NormGroup

# ✅ QnA
from .qna import QnA

# ✅ 인증 관련
from .verification_code import VerificationCode

# ✅ create_all에서 사용할 Base 포함
from backend.database.database import Base
