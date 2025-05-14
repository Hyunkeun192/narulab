# app/routers/notifications.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.test import TestTypeEnum  # optional
from pydantic import BaseModel
from app.models.notification import Notification  # 아래 모델 생성 필요
from typing import List
from datetime import datetime

router = APIRouter()


# ✅ DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ 알림 응답 스키마
class NotificationSchema(BaseModel):
    notification_id: str
    title: str
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True


# ✅ 알림 목록 조회 API
@router.get("/api/notifications", response_model=List[NotificationSchema])
def get_notifications(email: str, db: Session = Depends(get_db)):
    # 암호화된 이메일 기준 알림 조회
    notifications = db.query(Notification).filter(
        Notification.email == email
    ).order_by(Notification.created_at.desc()).all()

    return notifications

# ✅ 알림 읽음 처리 API
@router.post("/api/notifications/{notification_id}/read")
def mark_as_read(notification_id: str, db: Session = Depends(get_db)):
    # 알림 찾기
    notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    # 읽음 처리
    notification.is_read = True
    db.commit()

    return {"message": "Notification marked as read."}
