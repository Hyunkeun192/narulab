from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from uuid import UUID, uuid4
from typing import Optional, List

from backend.database.database import get_db
from backend.models.question import Question, QuestionStatus
from backend.models.option import Option
from backend.schemas.question_review import QuestionReviewRequest, QuestionReviewResponse
from backend.schemas.question_list import QuestionListItem
from backend.schemas.question_create import QuestionCreateRequest, QuestionCreateResponse

# ✅ 관리자 인증 의존성 (변경)
from backend.dependencies.admin_auth import get_content_or_super_admin_user

# ✅ 관리자 문항 관련 라우터 정의
router = APIRouter(
    prefix="/api/admin/questions",
    tags=["Admin - Questions"],
    dependencies=[Depends(get_content_or_super_admin_user)]  # 🔧 수정: content_admin 허용
)

# 🔍 AI 문항 승인/반려 처리 API
@router.post("/{question_id}/review", response_model=QuestionReviewResponse)
def review_question(
    question_id: UUID,
    request: QuestionReviewRequest,
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
        message = "Question reviewed and rejected."

    db.commit()
    return QuestionReviewResponse(message=message)

# 🔍 문항 목록 조회 API (상태별 필터 지원)
@router.get("", response_model=List[QuestionListItem])
def get_questions(
    status: Optional[QuestionStatus] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Question).options(joinedload(Question.options))
    if status:
        query = query.filter(Question.status == status)
    return query.order_by(Question.created_at.desc()).all()

# ✅ 문항 등록 API (선택지 포함)
@router.post("", response_model=QuestionCreateResponse)
def create_question(
    request: QuestionCreateRequest,
    db: Session = Depends(get_db)
):
    """
    ✅ 문항 등록 API
    - test_id 없이도 등록 가능
    - 외래키 오류 방지용 조건 포함
    """
    question_fields = {
        "question_id": uuid4(),
        "question_text": request.question_text,
        "question_type": request.question_type,
        "is_multiple_choice": request.is_multiple_choice,
        "instruction": request.instruction,
        "correct_explanation": request.correct_explanation,
        "wrong_explanation": request.wrong_explanation,
        "question_image_url": request.question_image_url,
        "question_name": request.question_name,
        "status": QuestionStatus.approved  # ✅ 관리자 등록 시 무조건 approved
    }

    if request.test_id:
        question_fields["test_id"] = request.test_id

    question = Question(**question_fields)
    db.add(question)
    db.flush()

    for index, opt in enumerate(request.options):
        option = Option(
            option_id=uuid4(),
            question_id=question.question_id,
            option_text=opt.option_text,
            is_correct=opt.is_correct,
            option_image_url=opt.option_image_url,
            option_order=index
        )
        db.add(option)

    db.commit()

    return QuestionCreateResponse(
        question_id=question.question_id,
        message="Question created successfully."
    )
