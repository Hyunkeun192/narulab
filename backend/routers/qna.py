from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models.qna import QnA
from backend.schemas.qna import QnACreate, QnAAnswer, QnAOut
from backend.dependencies.admin_auth import get_super_admin_user
from backend.dependencies.external_admin_auth import get_content_admin_user  # ✅ 콘텐츠 관리자 인증 함수
from backend.core.security import get_current_user
from backend.models.user import User
from datetime import datetime

router = APIRouter()

@router.get("/api/qna", response_model=list[QnAOut])
def get_qna_list(db: Session = Depends(get_db)):
    return db.query(QnA).order_by(QnA.created_at.desc()).all()

@router.post("/api/qna", response_model=QnAOut)
def post_question(
    qna: QnACreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)  # ✅ 일반 로그인 사용자만 질문 가능
):
    new_qna = QnA(
        question=qna.question,
        created_by=user.user_id
    )
    db.add(new_qna)
    db.commit()
    db.refresh(new_qna)
    return new_qna

# ✅ super admin 또는 contents admin만 답변 가능
def get_admin_user(
    super_admin: User = Depends(get_super_admin_user),
    content_admin: User = Depends(get_content_admin_user)
) -> User:
    """
    Super Admin 또는 콘텐츠 관리자 중 하나라도 통과하면 허용
    """
    return super_admin or content_admin

@router.put("/api/qna/{qna_id}/answer", response_model=QnAOut)
def answer_qna(
    qna_id: str,
    answer: QnAAnswer,
    db: Session = Depends(get_db),
    user: User = Depends(get_admin_user)  # ✅ super 또는 content admin 모두 허용
):
    qna = db.query(QnA).filter(QnA.id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    qna.answer = answer.answer
    qna.answered_by = user.user_id
    qna.answered_at = datetime.utcnow()
    db.commit()
    db.refresh(qna)
    return qna
