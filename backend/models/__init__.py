# app/models/__init__.py

from .user import User, UserProfile
from .institution_admin import *
from .notification import *
from .option import *
from .question import *
from .test import *
from .verification_code import VerificationCode  # ✅ 새로 추가한 인증 코드 모델

from backend.database.database import Base  # ✅ create_all_tables.py에서 사용됨
