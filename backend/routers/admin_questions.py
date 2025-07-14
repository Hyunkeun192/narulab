from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from uuid import UUID, uuid4
from typing import Optional, List

from backend.database.database import get_db
from backend.models.question import Question, QuestionStatus
from backend.models.option import Option
from backend.schemas.question_review import QuestionReviewRequest, QuestionReviewResponse
from backend.schemas.question_list import QuestionListItem, OptionItem
from backend.schemas.question_create import QuestionCreateRequest, QuestionCreateResponse
from backend.dependencies.admin_auth import get_current_admin_user

# ✅ 관리자 인증 의존성
from backend.dependencies.admin_auth import get_content_or_super_admin_user

router = APIRouter(
    prefix="/api/admin/questions",
    tags=["Admin - Questions"],
    dependencies=[Depends(get_content_or_super_admin_user)]
)

# ✅ 문항 상세 조회 (미리보기용) → 반드시 제일 위에 위치해야 FastAPI 라우팅 오류 방지
# ✅ 문항 상세 조회 (미리보기용) → 반드시 제일 위에 위치해야 FastAPI 라우팅 오류 방지
@router.get("/detail/{question_id}")
def get_question_by_id(
    question_id: UUID,
    db: Session = Depends(get_db)
):
    """
    ✅ 미리보기 기능용 단일 문항 조회 API
    - options 포함
    - MySQL에서는 UUID vs VARCHAR 비교 문제로 str 변환 필요
    """
    # 🔧 UUID → 문자열로 변환하여 비교해야 MySQL에서 매칭됨
    question = db.query(Question).filter(Question.question_id == str(question_id)).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    options = (
        db.query(Option)
        .filter(Option.question_id == str(question_id))
        .order_by(Option.option_order.asc())
        .all()
    )

    return {
        "question_id": question.question_id,
        "question_name": question.question_name,
        "instruction": question.instruction,
        "question_text": question.question_text,
        "options": [
            {
                "option_id": o.option_id,
                "option_text": o.option_text,
                "option_order": o.option_order
            }
            for o in options
        ]
    }

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
    """
    ✅ 문항 목록을 조회하고, 선택지에 option_order 포함되도록 명시적 직렬화 처리
    ✅ 프론트엔드 '문항 보기' 기능에서 option_order 기반 정렬을 위해 필요
    """
    query = db.query(Question).options(joinedload(Question.options))
    if status:
        query = query.filter(Question.status == status)

    questions = query.order_by(Question.created_at.desc()).all()

    result = []
    for q in questions:
        result.append(QuestionListItem(
            question_id=q.question_id,
            test_id=q.test_id,
            question_text=q.question_text,
            question_type=q.question_type,
            is_multiple_choice=q.is_multiple_choice,
            status=q.status,
            created_at=q.created_at,
            question_name=q.question_name,
            instruction=q.instruction,
            correct_explanation=q.correct_explanation,
            wrong_explanation=q.wrong_explanation,
            usage_type=q.usage_type,
            options=[
                OptionItem(
                    option_text=o.option_text,
                    is_correct=o.is_correct,
                    option_order=o.option_order
                ) for o in sorted(q.options, key=lambda x: x.option_order or 0)
            ]
        ))
    return result

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

    db.query(Option).filter(Option.question_id == str(question_id)).delete()
    db.query(Question).filter(Question.question_id == str(question_id)).delete()

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
        status=QuestionStatus.approved
    )
    db.add(new_question)
    db.flush()

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

@router.get("/{question_id}/used-in-tests", response_model=list[str])
def get_tests_using_question(
    question_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    해당 문항이 어떤 검사(test)에 연결되어 있는지 검사명 목록을 반환합니다.
    """
    from models.test_question_links import TestQuestionLink
    from models.test import Test

    # 연결된 검사 ID 가져오기
    links = db.query(TestQuestionLink).filter(TestQuestionLink.question_id == question_id).all()
    test_ids = [link.test_id for link in links]

    # 검사명 조회
    tests = db.query(Test).filter(Test.test_id.in_(test_ids)).all()
    return [t.test_name for t in tests]

# ✅ 문항 삭제 API
@router.delete("/{question_id}")  # 프론트엔드 요청 경로에 맞춰 DELETE 메서드 추가
def delete_question(
    question_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    ✅ 문항 삭제 API
    - 문항 ID에 해당하는 데이터 삭제
    - 삭제 전 연결된 options / responses / test_question_links를 함께 삭제 (FK 무결성 유지)
    """
    # 🔧 문자열로 변환 (MySQL UUID 저장형식 대응)
    question_id_str = str(question_id)

    # ✅ Option (선택지) 먼저 삭제
    db.query(Option).filter(Option.question_id == question_id_str).delete()

    # ✅ TestQuestionLink (검사-문항 연결) 먼저 삭제
    from backend.models.test_question_links import TestQuestionLink
    db.query(TestQuestionLink).filter(TestQuestionLink.question_id == question_id_str).delete()

    # ✅ Response (응답 데이터) 먼저 삭제
    from backend.models.response import UserResponse  # ❗️ 올바른 모델 import
    db.query(UserResponse).filter(UserResponse.question_id == question_id_str).delete()

    # ✅ Question (문항) 최종 삭제
    question = db.query(Question).filter(Question.question_id == question_id_str).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()

    return {"message": "Question and related data deleted successfully."}
