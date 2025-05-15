from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List

from database import get_db
from models.test import Test
from models.question import Question
from models.option import Option
from schemas.test_detail import TestDetailResponse, QuestionWithOptions
from schemas.test_create import TestCreateRequest, TestCreateResponse
from schemas.test_add_question import AddQuestionRequest, AddQuestionResponse
from schemas.test_remove_question import RemoveQuestionRequest, RemoveQuestionResponse
from schemas.test_update import TestUpdateRequest, TestUpdateResponse

# ✅ 관리자 인증 의존성 import
from dependencies.admin_auth import get_current_admin_user

# ✅ 관리자 인증 적용된 라우터
router = APIRouter(
    prefix="/api/admin/tests",
    tags=["Admin - Tests"],
    dependencies=[Depends(get_current_admin_user)]
)

# 🔍 특정 검사의 상세 구성 정보 조회 API
@router.get("/{test_id}", response_model=TestDetailResponse)
def get_test_detail(
    test_id: UUID,
    db: Session = Depends(get_db)
):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = (
        db.query(Question)
        .filter(Question.test_id == test_id)
        .order_by(Question.order_index)
        .all()
    )

    question_items: List[QuestionWithOptions] = []

    for q in questions:
        options = (
            db.query(Option)
            .filter(Option.question_id == q.question_id)
            .order_by(Option.option_order)
            .all()
        )

        question_items.append(
            QuestionWithOptions(
                question_id=q.question_id,
                question_text=q.question_text,
                question_type=q.question_type,
                is_multiple_choice=q.is_multiple_choice,
                status=q.status,
                options=options
            )
        )

    return TestDetailResponse(
        test_id=test.test_id,
        test_name=test.test_name,
        test_type=test.test_type,
        version=test.version,
        duration_minutes=test.duration_minutes,
        questions=question_items
    )


# ✅ 검사 등록 API
@router.post("/", response_model=TestCreateResponse)
def create_test(
    request: TestCreateRequest,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Test)
        .filter(Test.test_name == request.test_name, Test.version == request.version)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Test with same name and version already exists.")

    test = Test(
        test_id=uuid4(),
        test_name=request.test_name,
        test_type=request.test_type,
        version=request.version,
        duration_minutes=request.duration_minutes
    )
    db.add(test)
    db.commit()

    return TestCreateResponse(
        test_id=test.test_id,
        message="Test created successfully."
    )


# ✅ 검사에 문항 연결 API
@router.post("/{test_id}/add-question", response_model=AddQuestionResponse)
def add_questions_to_test(
    test_id: UUID,
    request: AddQuestionRequest,
    db: Session = Depends(get_db)
):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    added_count = 0

    for question_id in request.question_ids:
        question = db.query(Question).filter(Question.question_id == question_id).first()
        if question:
            question.test_id = test_id
            added_count += 1

    db.commit()

    return AddQuestionResponse(
        added_count=added_count,
        message=f"{added_count} questions added to test."
    )


# ✅ 검사에서 문항 제거 API
@router.post("/{test_id}/remove-question", response_model=RemoveQuestionResponse)
def remove_questions_from_test(
    test_id: UUID,
    request: RemoveQuestionRequest,
    db: Session = Depends(get_db)
):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    removed_count = 0

    for question_id in request.question_ids:
        question = db.query(Question).filter(
            Question.question_id == question_id,
            Question.test_id == test_id
        ).first()
        if question:
            question.test_id = None
            removed_count += 1

    db.commit()

    return RemoveQuestionResponse(
        removed_count=removed_count,
        message=f"{removed_count} questions removed from test."
    )


# ✅ 검사 정보 수정 API
@router.put("/{test_id}", response_model=TestUpdateResponse)
def update_test(
    test_id: UUID,
    request: TestUpdateRequest,
    db: Session = Depends(get_db)
):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    if request.test_name is not None:
        test.test_name = request.test_name
    if request.test_type is not None:
        test.test_type = request.test_type
    if request.version is not None:
        test.version = request.version
    if request.duration_minutes is not None:
        test.duration_minutes = request.duration_minutes
    if request.scoring_rule_id is not None:
        test.scoring_rule_id = request.scoring_rule_id
    if request.norm_group_id is not None:
        test.norm_group_id = request.norm_group_id

    db.commit()

    return TestUpdateResponse(
        test_id=test.test_id,
        message="Test updated successfully."
    )
