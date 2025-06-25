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

# ✅ 관리자 인증 의존성
from backend.dependencies.admin_auth import get_content_or_super_admin_user

router = APIRouter(
    prefix="/api/admin/questions",
    tags=["Admin - Questions"],
    dependencies=[Depends(get_content_or_super_admin_user)]
)

# 🔍 문항 승인/반려
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

# 🔍 문항 목록 조회
@router.get("", response_model=List[QuestionListItem])
def get_questions(
    status: Optional[QuestionStatus] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Question).options(joinedload(Question.options))
    if status:
        query = query.filter(Question.status == status)
    return query.order_by(Question.created_at.desc()).all()

# ✅ 문항 등록
@router.post("", response_model=QuestionCreateResponse)
def create_question(
    request: QuestionCreateRequest,
    db: Session = Depends(get_db)
):
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
        "usage_type": request.usage_type,
        "status": QuestionStatus.approved
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

# ✅ 문항 수정 (문항 + 선택지 전체 업데이트)
@router.put("/{question_id}", response_model=QuestionCreateResponse)
def update_question(
    question_id: UUID,
    request: QuestionCreateRequest,
    db: Session = Depends(get_db)
):
    print(f"🚨 update_question 호출됨: question_id = {question_id} ({type(question_id)})")

    # 기존 문항 및 연결된 선택지 제거
    db.query(Option).filter(Option.question_id == str(question_id)).delete()
    db.query(Question).filter(Question.question_id == str(question_id)).delete()

    # 새 문항 객체 생성 및 삽입
    new_question = Question(
        question_id=str(question_id),
        test_id=request.test_id,
        question_text=request.question_text,
        question_type=request.question_type,
        is_multiple_choice=request.is_multiple_choice,
        instruction=request.instruction,
        correct_explanation=request.correct_explanation,
        wrong_explanation=request.wrong_explanation,
        question_image_url=request.question_image_url,
        question_name=request.question_name,
        usage_type=request.usage_type,
        status=QuestionStatus.approved  # 수정도 승인 상태로 고정
    )
    db.add(new_question)
    db.flush()  # question_id 확정

    # 새 선택지 삽입
    for index, opt in enumerate(request.options):
        new_option = Option(
            option_id=uuid4(),
            question_id=str(question_id),
            option_text=opt.option_text,
            is_correct=opt.is_correct,
            option_image_url=opt.option_image_url,
            option_order=index
        )
        db.add(new_option)

    db.commit()

    return QuestionCreateResponse(
        question_id=question_id,
        message="Question updated successfully (replaced)."
    )
