# app/models/verification_code.py

from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime, timedelta
from backend.database.database import Base

class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String(255), nullable=False)  # 이메일 또는 전화번호
    type = Column(String(10), nullable=False)     # "email" or "phone"
    code = Column(String(5), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at
