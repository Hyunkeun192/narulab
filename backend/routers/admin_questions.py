# /Users/hyunkeunkim/Desktop/narulab/backend/routers/admin_questions.py

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

# ✅ 관리자 문항 관련 라우터 정의
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
    # ✅ 문항 조회
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # ✅ 승인 또는 반려 처리
    if request.approved:
        question.status = QuestionStatus.approved
        question.review_comment = None
        message = "Question approved."
    else:
        question.status = QuestionStatus.rejected
        question.review_comment = request.review_comment or "No comment provided."
        message = "Question reviewed and rejected."

    # ✅ DB 반영
    db.commit()
    return QuestionReviewResponse(message=message)


# 🔍 문항 목록 조회 API (상태별 필터 지원)
@router.get("", response_model=List[QuestionListItem])
def get_questions(
    status: Optional[QuestionStatus] = Query(None),  # ?status=waiting 등 필터
    db: Session = Depends(get_db)                    # DB 세션 주입
):
    query = db.query(Question)

    # ✅ 상태 필터링이 있을 경우 적용
    if status:
        query = query.filter(Question.status == status)

    # ✅ 최신순 정렬하여 반환
    return query.order_by(Question.created_at.desc()).all()


# ✅ 문항 등록 API (선택지 포함) → test_id 없이도 등록 가능하도록 수정됨
@router.post("", response_model=QuestionCreateResponse)
def create_question(
    request: QuestionCreateRequest,
    db: Session = Depends(get_db)
):
    """
    ✅ 문항 등록 API (test_id 없이 문항 풀 형태로도 저장 가능)
    - 기존에는 test_id가 필수였으나, 이제는 없어도 등록 가능하도록 수정
    - FK 오류 방지를 위해 test_id가 존재하고 실제 유효한 경우에만 포함
    """

    # ✅ 필드 정의용 dict 생성 (test_id 조건부 포함 위해 분리)
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
        "status": QuestionStatus.waiting
    }

    # ✅ test_id가 실제로 존재하고 빈 문자열/None이 아닌 경우만 포함
    if request.test_id and str(request.test_id).strip() not in ("", "null", "None"):
        question_fields["test_id"] = request.test_id

    # ✅ Question 객체 생성
    question = Question(**question_fields)
    db.add(question)
    db.flush()  # question_id 확보용

    # ✅ 선택지 저장
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

    # ✅ 최종 커밋
    db.commit()

    # ✅ 응답 반환
    return QuestionCreateResponse(
        question_id=question.question_id,
        message="Question created successfully."
    )
