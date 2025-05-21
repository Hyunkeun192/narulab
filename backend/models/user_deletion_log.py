from sqlalchemy import Column, String, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from backend.database.database import Base

# ✅ 사용자 탈퇴 로그 테이블 정의
class UserDeletionLog(Base):
    __tablename__ = "user_deletion_logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=False)
    last_company = Column(String(100), nullable=True)
    reason = Column(Text, nullable=True)
