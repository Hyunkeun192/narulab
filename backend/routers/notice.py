# routers/notice.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.notice import NoticeOut
from backend.models.notice import Notice
from backend.database.database import get_db

router = APIRouter()

@router.get("/api/notices", response_model=list[NoticeOut])
def get_notices(db: Session = Depends(get_db)):
    return db.query(Notice).order_by(Notice.created_at.desc()).all()
