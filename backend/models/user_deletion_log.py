# backend/models/user_deletion_log.py

from sqlalchemy import Column, Integer, TIMESTAMP, Text, ForeignKey, String
from uuid import uuid4
from backend.database.database import Base

# ✅ 사용자 탈퇴 로그 테이블 정의
class UserDeletionLog(Base):
    __tablename__ = "user_deletion_logs"

    log_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # 로그 식별용 UUID
    user_id = Column(Integer, ForeignKey("users.id"))  # 🔁 users.id는 int 타입
    deleted_at = Column(TIMESTAMP, nullable=False)  # 탈퇴 일시
    last_company = Column(String(100), nullable=True)  # 마지막 근무 회사
    reason = Column(Text, nullable=True)  # 탈퇴 사유
