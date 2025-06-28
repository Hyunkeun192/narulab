from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List, Any

from backend.database.database import get_db
from backend.models.test import Test
from backend.models.question import Question
from backend.models.option import Option
from backend.schemas.question_create import OptionItem
from backend.schemas.test_detail import TestDetailResponse, QuestionWithOptionsOut, QuestionIdList, TestCreateRequest
from backend.schemas.test_create import TestCreateRequest, TestCreateResponse
from backend.schemas.test_add_question import AddQuestionRequest, AddQuestionResponse
from backend.schemas.test_remove_question import RemoveQuestionRequest, RemoveQuestionResponse
from backend.schemas.test_update import TestUpdateRequest, TestUpdateResponse
from backend.schemas.test_question_bulk_link import TestQuestionBulkLinkRequest

from backend.dependencies.admin_auth import get_current_admin_user

from backend.models.test_question_links import TestQuestionLink
from backend.schemas.test_question_links import TestQuestionLinkCreate, TestQuestionLinkOut



router = APIRouter(
    prefix="/api/admin/tests",
    tags=["Admin - Tests"],
    dependencies=[Depends(get_current_admin_user)]
)


# ✅ 전체 검사 목록 조회
@router.get("", response_model=List[TestCreateResponse])
def get_all_tests(db: Session = Depends(get_db)):
    tests = db.query(Test).all()
    return [
        TestCreateResponse(
            test_id=test.test_id,
            message=test.test_name
        )
        for test in tests
    ]


# ✅ 특정 검사 상세 조회
@router.get("/{test_id}", response_model=TestDetailResponse)
def get_test_detail(test_id: UUID, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.test_id == str(test_id)).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = (
        db.query(Question)
        .filter(Question.test_id == str(test_id))
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
        question_items.append(
            QuestionWithOptions(
                question_id=q.question_id,
                question_name=q.question_name,
                question_text=q.question_text,
                instruction=q.instruction,
                question_type=q.question_type,
                is_multiple_choice=q.is_multiple_choice,
                correct_explanation=q.correct_explanation,
                wrong_explanation=q.wrong_explanation,
                status=q.status,
                options=option_items
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


# ✅ 검사 등록
@router.post("/", response_model=TestCreateResponse)
def create_test(
    request: TestCreateRequest = Body(...),
    db: Session = Depends(get_db),
    local_kw: str = Query(..., alias="local_kw")
):
    existing = db.query(Test).filter(
        Test.test_name == request.test_name,
        Test.version == request.version
    ).first()

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


# ✅ 검사에 기존 방식으로 문항 추가
@router.post("/{test_id}/add-question", response_model=AddQuestionResponse)
def add_questions_to_test(
    test_id: UUID,
    request: AddQuestionRequest,
    db: Session = Depends(get_db)
):
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


# ✅ 검사에서 문항 제거
@router.post("/{test_id}/remove-question", response_model=RemoveQuestionResponse)
def remove_questions_from_test(
    test_id: UUID,
    request: RemoveQuestionRequest,
    db: Session = Depends(get_db)
):
    test = db.query(Test).filter(Test.test_id == str(test_id)).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    removed_count = 0
    for question_id in request.question_ids:
        question = db.query(Question).filter(
            Question.question_id == question_id,
            Question.test_id == str(test_id)
        ).first()
        if question:
            question.test_id = None
            removed_count += 1

    db.commit()

    return RemoveQuestionResponse(
        removed_count=removed_count,
        message=f"{removed_count} questions removed from test."
    )


# ✅ 검사 정보 수정
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


# ✅ 문항 일괄 연결 API (test_question_links 사용)
@router.post("/{test_id}/questions")
def bulk_link_questions_to_test(
    test_id: str,
    question_data: QuestionIdList,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user),
):
    """
    테스트에 문항 일괄 연결
    기존 연결 삭제 후 새로 저장
    """
    # 기존 연결 삭제
    db.query(TestQuestionLink).filter(TestQuestionLink.test_id == test_id).delete()
    db.commit()

    question_ids = question_data.question_ids
    new_links = []

    for idx, q_id in enumerate(question_ids):
        link = TestQuestionLink(
            test_id=test_id,
            question_id=q_id,
            order_index=idx,
        )
        db.add(link)
        new_links.append(link)

    db.commit()

    # ✅ 등록된 문항 수 업데이트
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if test:
        test.question_count = (
            db.query(TestQuestionLink)
            .filter(TestQuestionLink.test_id == test_id)
            .count()
        )
        db.commit()

    # ✅ 응답 형식도 변경
    return {"message": "문항이 성공적으로 연결되었습니다."}



# ✅ 문항 리스트 조회 라우터 - 등록된 문항 확인/수정용
@router.get("/{test_id}/questions", response_model=list[QuestionWithOptionsOut])
def get_test_questions(test_id: str, db: Session = Depends(get_db), user=Depends(get_current_admin_user)):
    """
    특정 검사에 연결된 문항과 보기(option)를 순서대로 반환합니다.
    """
    links = (
        db.query(TestQuestionLink)
        .filter(TestQuestionLink.test_id == test_id)
        .order_by(TestQuestionLink.order_index)
        .all()
    )

    questions = []
    for link in links:
        question = db.query(Question).filter(Question.question_id == link.question_id).first()
        if question:
            options = db.query(Option).filter(Option.question_id == question.question_id).all()
            question.options = options
            questions.append(question)

    return questions

@router.put("/{test_id}/publish")
def toggle_publish_test(
    test_id: str,
    publish: bool = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    검사 활성화 여부 변경 (활성화: True, 비활성화: False)
    """
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="검사를 찾을 수 없습니다.")

    test.is_published = 1 if publish else 0
    db.commit()

    return {
        "success": True,
        "test_id": test_id,
        "is_published": test.is_published
    }