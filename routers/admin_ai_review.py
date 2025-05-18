from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from uuid import UUID

from database.database import get_db
from models.question import Question, QuestionStatus
from models.option import Option
from schemas.ai_review import (
    AIQuestionListItem,
    AIQuestionDetail,
    AIReviewRequest,
    AIReviewResponse,
)

# ✅ 관리자 인증 의존성 import
from dependencies.admin_auth import get_current_admin_user

# 관리자 AI 문항 검토 라우터
router = APIRouter(
    prefix="/api/admin/ai-review",
    tags=["Admin - AI Review"],
    dependencies=[Depends(get_current_admin_user)]  # ✅ 관리자 인증 적용
)

# ✅ 목록 조회 (상태 필터링 가능)
@router.get("/", response_model=List[AIQuestionListItem])
def get_ai_questions(
    status: Optional[QuestionStatus] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Question).filter(Question.question_text != None)  # AI 문항으로 간주

    if status:
        query = query.filter(Question.status == status)

    return query.order_by(Question.question_id.desc()).all()

# ✅ 문항 상세 조회
@router.get("/{question_id}", response_model=AIQuestionDetail)
def get_ai_question_detail(
    question_id: UUID,
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    options = (
        db.query(Option)
        .filter(Option.question_id == question_id)
        .order_by(Option.option_order)
        .all()
    )

    return AIQuestionDetail(
        question_id=question.question_id,
        question_text=question.question_text,
        question_type=question.question_type,
        is_multiple_choice=question.is_multiple_choice,
        options=[{
            "option_text": o.option_text,
            "is_correct": o.is_correct
        } for o in options],
        ai_explanation=None,
        status=question.status,
        review_comment=question.review_comment
    )

# ✅ 문항 승인/반려 처리
@router.post("/{question_id}/review", response_model=AIReviewResponse)
def review_ai_question(
    question_id: UUID,
    request: AIReviewRequest,
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if request.approved:
        question.status = QuestionStatus.approved
        question.review_comment = None
        message = "Question approved."
    else:
        question.status = QuestionStatus.rejected
        question.review_comment = request.review_comment or "No comment provided."
        message = "Question rejected."

    db.commit()
    return AIReviewResponse(message=message)
