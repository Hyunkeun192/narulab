from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.notice import NoticeOut, NoticeCreate, NoticeUpdate
from backend.models.notice import Notice
from backend.database.database import get_db
from backend.dependencies.admin_auth import get_super_admin_user
from backend.models.user import User

router = APIRouter()

@router.get("/api/notices", response_model=list[NoticeOut])
def get_notices(db: Session = Depends(get_db)):
    return db.query(Notice).order_by(Notice.created_at.desc()).all()

@router.post("/api/notices", response_model=NoticeOut, status_code=status.HTTP_201_CREATED)
def create_notice(notice: NoticeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_super_admin_user)):
    new_notice = Notice(title=notice.title, content=notice.content, created_by=current_user.user_id)
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return new_notice

@router.put("/api/notices/{notice_id}", response_model=NoticeOut)
def update_notice(notice_id: int, notice: NoticeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_super_admin_user)):
    db_notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not db_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    db_notice.title = notice.title
    db_notice.content = notice.content
    db.commit()
    db.refresh(db_notice)
    return db_notice

@router.delete("/api/notices/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notice(notice_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_super_admin_user)):
    db_notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not db_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    db.delete(db_notice)
    db.commit()
    return None
