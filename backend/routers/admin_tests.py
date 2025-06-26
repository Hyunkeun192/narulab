from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List, Any

from backend.database.database import get_db
from backend.models.test import Test
from backend.models.question import Question
from backend.models.option import Option
from backend.schemas.question_create import OptionItem  # ✅ Pydantic 변환용 모델
from backend.schemas.test_detail import TestDetailResponse, QuestionWithOptions
from backend.schemas.test_create import TestCreateRequest, TestCreateResponse
from backend.schemas.test_add_question import AddQuestionRequest, AddQuestionResponse
from backend.schemas.test_remove_question import RemoveQuestionRequest, RemoveQuestionResponse
from backend.schemas.test_update import TestUpdateRequest, TestUpdateResponse
from backend.schemas.test_question_bulk_link import TestQuestionBulkLinkRequest  # ✅ 이 줄 추가


# ✅ 관리자 인증 의존성 import
from backend.dependencies.admin_auth import get_current_admin_user

# ✅ 검사-문항 연결용 모델 및 스키마 import
from backend.models.test_question_links import TestQuestionLink
from backend.schemas.test_question_links import TestQuestionLinkCreate, TestQuestionLinkOut

# ✅ 관리자 인증 적용된 라우터
router = APIRouter(
    prefix="/api/admin/tests",
    tags=["Admin - Tests"],
    dependencies=[Depends(get_current_admin_user)]
)

# ✅ 전체 검사 목록 조회 API (프론트에서 GET /api/admin/tests 요청 시 사용)
@router.get("", response_model=List[TestCreateResponse])
def get_all_tests(db: Session = Depends(get_db)):
    """
    ✅ 전체 검사 목록을 조회하는 API
    - GET /api/admin/tests 요청 대응
    - 프론트엔드에서 검사 리스트 드롭다운 등에 활용 가능
    """
    tests = db.query(Test).all()
    return [
        TestCreateResponse(
            test_id=test.test_id,
            message=test.test_name  # ✅ message 필드를 test_name으로 임시 전송
        )
        for test in tests
    ]

# 🔍 특정 검사의 상세 구성 정보 조회 API
@router.get("/{test_id}", response_model=TestDetailResponse)
def get_test_detail(
    test_id: UUID,
    db: Session = Depends(get_db)
):
    test = db.query(Test).filter(Test.test_id == str(test_id)).first()  # UUID → str 변환
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    questions = (
        db.query(Question)
        .filter(Question.test_id == str(test_id))  # UUID → str 변환
        .order_by(Question.order_index)
        .all()
    )

    question_items: List[QuestionWithOptions] = []

    for q in test.questions:
        option_items = [
            OptionItem(
                option_id=o.option_id,
                option_order=o.option_order,
                option_text=o.option_text,
                is_correct=o.is_correct,
                option_image_url=o.option_image_url
            )
        for o in q.options
        ]

    questions.append(
        QuestionWithOptions(
            question_id=q.question_id,
            question_name=q.question_name,
            question_text=q.question_text,
            instruction=q.instruction,
            question_type=q.question_type,
            is_multiple_choice=q.is_multiple_choice,
            correct_explanation=q.correct_explanation,
            wrong_explanation=q.wrong_explanation,
            status=q.status,  # ✅ 누락된 필드 보완
            options=option_items
        )
    )

    return TestDetailResponse(
        test_id=test.test_id,
        test_name=test.test_name,
        test_type=test.test_type,
        version=test.version,
        duration_minutes=test.duration_minutes,
        questions=questions  # ✅ 응답 필드와 변수 이름 일치
    )

# ✅ 검사 등록 API
@router.post("/", response_model=TestCreateResponse)
def create_test(
    request: TestCreateRequest = Body(...),
    db: Session = Depends(get_db),
    local_kw: str = Query(..., alias="local_kw")
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

# ✅ 검사에 문항 연결 API (test_id 기준 직접 연결용)
@router.post("/{test_id}/add-question", response_model=AddQuestionResponse)
def add_questions_to_test(
    test_id: UUID,
    request: AddQuestionRequest,
    db: Session = Depends(get_db)
):
    # ✅ UUID → str로 변환하여 비교 (CHAR 필드 호환)
    test = db.query(Test).filter(Test.test_id == str(test_id)).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    added_count = 0

    for question_id in request.question_ids:
        question = db.query(Question).filter(Question.question_id == str(question_id)).first()
        if question and question.test_id is None:
            question.test_id = str(test_id)
            db.add(question)
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
    test = db.query(Test).filter(Test.test_id == str(test_id)).first()  # ← 수정 필요
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    removed_count = 0

    for question_id in request.question_ids:
        question = db.query(Question).filter(
            Question.question_id == question_id,
            Question.test_id == str(test_id)  # ✅ 문자열로 변환
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

# ✅ 신규 추가: test_question_links 테이블 기반 문항 연결용 API
@router.post("/{test_id}/questions", response_model=List[TestQuestionLinkOut])
def bulk_link_questions_to_test(
    test_id: UUID,
    request: TestQuestionBulkLinkRequest = Body(...),
    db: Session = Depends(get_db)
):
    """
    ✅ 기존 문항 삭제 후 새로운 문항들을 순서대로 검사에 연결
    """
    test = db.query(Test).filter(Test.test_id == str(test_id)).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    # 기존 연결 모두 삭제
    db.query(TestQuestionLink).filter(TestQuestionLink.test_id == str(test_id)).delete()

    # 새 연결 추가
    new_links = []
    for index, question_id in enumerate(request.question_ids):
        link = TestQuestionLink(
            test_id=str(test_id),
            question_id=question_id,
            order_index=index
        )
        db.add(link)
        new_links.append(link)

    db.commit()
    return new_links
