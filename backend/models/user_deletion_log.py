from sqlalchemy import Column, String, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from backend.database.database import Base

# ✅ 사용자 탈퇴 로그 테이블 정의
class UserDeletionLog(Base):
    __tablename__ = "user_deletion_logs"

    log_id = Column(String(36), primary_key=True)       # UUID → String(36)
    user_id = Column(String(36), ForeignKey("users.user_id") )    
    deleted_at = Column(TIMESTAMP, nullable=False)
    last_company = Column(String(100), nullable=True)
    reason = Column(Text, nullable=True)
