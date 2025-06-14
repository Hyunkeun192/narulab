# backend/models/user_deletion_log.py

from sqlalchemy import Column, String, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from backend.database.database import Base

# ✅ 사용자 탈퇴 로그 테이블 정의
class UserDeletionLog(Base):
    __tablename__ = "user_deletion_logs"

    log_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # ✅ UUID 문자열 기본값 설정
    user_id = Column(String(36), ForeignKey("users.id"))  # ✅ users 테이블의 PK(id)를 참조하도록 수정
    deleted_at = Column(TIMESTAMP, nullable=False)  # ✅ 탈퇴 일시
    last_company = Column(String(100), nullable=True)  # ✅ 마지막 근무 회사 (선택)
    reason = Column(Text, nullable=True)  # ✅ 탈퇴 사유 (자유 텍스트)
