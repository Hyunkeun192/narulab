# backend/models/user_deletion_log.py

from sqlalchemy import Column, String, TIMESTAMP, Text, ForeignKey
from uuid import uuid4
from backend.database.database import Base

# ✅ 사용자 탈퇴 로그 테이블 정의
class UserDeletionLog(Base):
    __tablename__ = "user_deletion_logs"

    log_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # ✅ 로그 식별용 UUID

    # 🔧 수정됨: 외래키 참조를 users.user_id로 변경하고, 타입을 String(36)으로 일치시킴
    user_id = Column(String(36), ForeignKey("users.user_id"))  # ✅ UUID 기반 사용자 식별자 참조

    deleted_at = Column(TIMESTAMP, nullable=False)  # ✅ 탈퇴 일시
    last_company = Column(String(100), nullable=True)  # ✅ 마지막 근무 회사
    reason = Column(Text, nullable=True)  # ✅ 탈퇴 사유
