from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models.notice import Notice
from backend.schemas.notice import NoticeCreate, NoticeUpdate, NoticeOut
from backend.dependencies.admin_auth import get_current_user
from backend.models.user import User
from uuid import uuid4
from typing import List

router = APIRouter(prefix="/api/notices", tags=["공지사항"])

# ✅ 공지사항 전체 조회 (모든 사용자 접근 가능)
@router.get("/", response_model=List[NoticeOut])
def get_notices(db: Session = Depends(get_db)):
    return db.query(Notice).order_by(Notice.created_at.desc()).all()

# ✅ 공지사항 생성 (super admin만 가능)
@router.post("/", response_model=NoticeOut)
def create_notice(
    notice_in: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ [수정] 기존: current_user.is_super_admin → role 필드 기반으로 명시적 확인
    if current_user.role != "super_admin":
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    new_notice = Notice(
        id=str(uuid4()),  # ✅ UUID 생성
        title=notice_in.title,
        content=notice_in.content,
        creator_id=current_user.user_id  # ✅ [수정] 필드명 user_id로 통일
    )
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return new_notice

# ✅ 공지사항 수정 (super admin만 가능)
@router.put("/{notice_id}", response_model=NoticeOut)
def update_notice(
    notice_id: str,
    notice_in: NoticeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ [수정] 권한 확인 방식 변경: role 필드 기반 확인
    if current_user.role != "super_admin":
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")

    notice.title = notice_in.title
    notice.content = notice_in.content
    db.commit()
    db.refresh(notice)
    return notice

# ✅ 공지사항 삭제 (super admin만 가능)
@router.delete("/{notice_id}")
def delete_notice(
    notice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ [수정] 권한 확인 방식 변경: role 필드 기반 확인
    if current_user.role != "super_admin":
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")

    db.delete(notice)
    db.commit()
    return {"message": "삭제 완료"}
