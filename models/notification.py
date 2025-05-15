# app/models/notification.py

import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from database.database import Base


# ✅ 사용자 알림 테이블
class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    email = Column(String(255), nullable=False)  # 암호화된 이메일 (FK 형태로 사용됨)
    
    title = Column(String(200), nullable=False)  # 알림 제목
    content = Column(String(500), nullable=False)  # 알림 본문 내용

    is_read = Column(Boolean, default=False)  # 읽음 여부
    created_at = Column(DateTime, default=datetime.utcnow)  # 생성 시각
