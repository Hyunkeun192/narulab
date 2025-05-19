from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import Optional, List

from backend.database.database import get_db
from backend.models.question import Question, QuestionStatus
from backend.models.option import Option
from backend.schemas.question_review import QuestionReviewRequest, QuestionReviewResponse
from backend.schemas.question_list import QuestionListItem
from backend.schemas.question_create import QuestionCreateRequest, QuestionCreateResponse

# ✅ 관리자 인증 의존성 import
from backend.dependencies.admin_auth import get_current_admin_user

# 관리자 문항 관련 라우터 정의
router = APIRouter(
    prefix="/api/admin/questions",
    tags=["Admin - Questions"],
    dependencies=[Depends(get_current_admin_user)]  # ✅ 관리자 인증 적용
)

# 🔍 AI 문항 승인/반려 처리 API
@router.post("/{question_id}/review", response_model=QuestionReviewResponse)
def review_question(
    question_id: UUID,                    # 검토할 문항의 UUID
    request: QuestionReviewRequest,      # 승인 여부 + 코멘트 요청 스키마
    db: Session = Depends(get_db)        # SQLAlchemy DB 세션 주입
):
    # 문항 조회
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # 승인 처리
    if request.approved:
        question.status = QuestionStatus.approved
        question.review_comment = None
        message = "Question approved."
    # 반려 처리
    else:
        question.status = QuestionStatus.rejected
        question.review_comment = request.review_comment or "No comment provided."
        message = "Question reviewed and rejected."

    # DB 반영
    db.commit()
    return QuestionReviewResponse(message=message)


# 🔍 문항 목록 조회 API (상태별 필터 지원)
@router.get("/", response_model=List[QuestionListItem])
def get_questions(
    status: Optional[QuestionStatus] = Query(None),  # ?status=waiting 등 필터
    db: Session = Depends(get_db)                    # DB 세션 주입
):
    query = db.query(Question)

    # 상태 필터링이 있을 경우
    if status:
        query = query.filter(Question.status == status)

    # 최신순 정렬하여 반환
    return query.order_by(Question.created_at.desc()).all()


# ✅ 문항 등록 API (선택지 포함)
@router.post("/", response_model=QuestionCreateResponse)
def create_question(
    request: QuestionCreateRequest,
    db: Session = Depends(get_db)
):
    # 새로운 문항 생성
    question = Question(
        question_id=uuid4(),
        test_id=request.test_id,
        question_text=request.question_text,
        question_type=request.question_type,
        is_multiple_choice=request.is_multiple_choice,
        status=QuestionStatus.waiting  # 기본 상태는 승인 대기
    )
    db.add(question)
    db.flush()  # question_id 확보용

    # 선택지들 저장
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
