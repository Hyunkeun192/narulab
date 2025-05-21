# app/routers/subscribe.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, get_db
from pydantic import BaseModel

router = APIRouter()

# ✅ 구독 응답 스키마
class SubscribeStatus(BaseModel):
    email: str
    plan: str  # "Free" 또는 "Pro"
    next_payment_due: str  # 예: YYYY-MM-DD or "-" if 없음

    class Config:
        orm_mode = True


# ✅ 구독 상태 조회 API
@router.get("/api/subscribe", response_model=SubscribeStatus)
def get_subscription(email: str, db: Session = Depends(get_db)):
    # TODO: 실제 구독 테이블이 있다면 그쪽에서 확인
    # 현재는 임시 값 반환
    return SubscribeStatus(
        email=email,
        plan="Free",
        next_payment_due="-"
    )
