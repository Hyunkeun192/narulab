from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models.qna import QnA
from backend.schemas.qna import QnACreate, QnAAnswer, QnAOut
from backend.dependencies.admin_auth import get_super_admin_user
from backend.dependencies.external_admin_auth import get_content_admin_user
from backend.core.security import get_current_user
from backend.models.user import User
from datetime import datetime

router = APIRouter()

# ✅ 관리자 인증: super admin 또는 콘텐츠 관리자 중 하나라도 인증되면 통과
def get_admin_user(
    super_admin: User = Depends(get_super_admin_user),
    content_admin: User = Depends(get_content_admin_user)
) -> User:
    return super_admin or content_admin

# ✅ QnA 전체 목록 조회 (권한에 따라 결과 달라짐)
@router.get("/api/qna", response_model=list[QnAOut])
def get_qna_list(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # ✅ super_admin 또는 content_admin은 전체 QnA 조회 가능
    if user.is_super_admin or user.is_content_admin:
        return db.query(QnA).order_by(QnA.created_at.desc()).all()

    # ✅ 일반 사용자는 공개된 QnA만 조회
    return (
        db.query(QnA)
        .filter(QnA.is_private == False)
        .order_by(QnA.created_at.desc())
        .all()
    )

# ✅ 사용자 QnA 등록 API
@router.post("/api/qna", response_model=QnAOut)
def post_question(
    qna: QnACreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # ✅ 작성자(user)의 ID를 created_by로 저장, 공개 여부도 함께 저장
    new_qna = QnA(
        created_by=user.id,
        question=qna.question,
        is_private=qna.is_private
    )
    db.add(new_qna)
    db.commit()
    db.refresh(new_qna)
    return new_qna

# ✅ 관리자 답변 등록 API
@router.put("/api/qna/{qna_id}/answer", response_model=QnAOut)
def answer_qna(
    qna_id: str,  # ✅ UUID 문자열로 처리
    answer: QnAAnswer,
    db: Session = Depends(get_db),
    user: User = Depends(get_admin_user)
):
    # ✅ 해당 QnA 조회
    qna = db.query(QnA).filter(QnA.id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA not found")

    # ✅ 답변 등록 및 관리자 정보 갱신
    qna.answer = answer.answer
    qna.answered_by = user.id
    qna.answered_at = datetime.utcnow()
    db.commit()
    db.refresh(qna)
    return qna
