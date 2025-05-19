from sqlalchemy import Column, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from backend.database.database import Base

class InstitutionAdmin(Base):
    __tablename__ = "institution_admins"

    admin_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    institution_type = Column(Enum("school", "company"), nullable=False)  # ✅ 학교 or 기업
    institution_name = Column(String(255), nullable=False)  # ✅ 학교명 or 회사명
    approved = Column(Boolean, default=False)  # ✅ 승인된 관리자 여부
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="institution_admin_profile")
