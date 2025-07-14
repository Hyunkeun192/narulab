from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
# ✅ Report → TestReport로 이름 변경하여 중복 오류 해결
from backend.models.test import Test, Question, Option, TestReport
from backend.models.test_analytics_by_group import TestAnalyticsByGroup, GroupTypeEnum
from backend.models.question_stats_by_group import QuestionStatsByGroup
from backend.models.sten_rule import STENRule  # ✅ STEN 등급 규칙 모델 import
from backend.models.user import UserProfile, User  # ✅ 사용자 정보 및 프로필
from backend.dependencies.admin_auth import get_current_user, get_current_admin_user  # ✅ 관리자 권한 확인 추가
from typing import List
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import uuid
import json

router = APIRouter()

# ✅ 검사 유형 enum
class TestTypeEnum(str, Enum):
    aptitude = "aptitude"
    personality = "personality"

# ✅ 검사 목록 응답용 스키마
class TestSummary(BaseModel):
    test_id: str
    test_name: str
    test_type: TestTypeEnum
    duration_minutes: int
    version: str

    class Config:
        model_config = {
        "from_attributes": True
    }

# ✅ 선택지 응답용 스키마
class OptionSchema(BaseModel):
    option_id: str
    option_text: str
    option_order: int

    class Config:
        model_config = {
        "from_attributes": True
    }

# ✅ 문항 응답용 스키마
class QuestionSchema(BaseModel):
    question_id: str
    question_text: str
    question_type: str
    is_multiple_choice: bool
    order_index: int
    options: List[OptionSchema]

    class Config:
        model_config = {
        "from_attributes": True
    }

# ✅ 검사 상세 조회용 스키마
class TestDetail(BaseModel):
    test_id: str
    test_name: str
    duration_minutes: int
    questions: List[QuestionSchema]

    class Config:
        model_config = {
        "from_attributes": True
    }

# ✅ 전체 검사 목록 조회
@router.get("/api/tests")
def get_tests(db: Session = Depends(get_db)):
    tests = db.query(Test).order_by(Test.created_at.desc()).all()
    return [
        {
            "test_id": t.test_id,
            "test_name": t.test_name,
            "test_type": t.test_type,
            "is_published": t.is_published,
            "question_count": t.question_count,  # ✅ 핵심 필드
            "duration_minutes": t.duration_minutes,
            "version": t.version
        }
        for t in tests
    ]

# ✅ 단일 검사 상세 조회
@router.get("/api/tests/{test_id}", response_model=TestDetail)
def get_test_detail(test_id: str, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = db.query(Question).filter(Question.test_id == test_id).order_by(Question.order_index).all()
    question_data = []
    for q in questions:
        options = db.query(Option).filter(Option.question_id == q.question_id).order_by(Option.option_order).all()
        question_data.append(QuestionSchema(
            question_id=q.question_id,
            question_text=q.question_text,
            question_type=q.question_type,
            is_multiple_choice=q.is_multiple_choice,
            order_index=q.order_index,
            options=[
                OptionSchema(
                    option_id=opt.option_id,
                    option_text=opt.option_text,
                    option_order=opt.option_order
                ) for opt in options
            ]
        ))

    return TestDetail(
        test_id=test.test_id,
        test_name=test.test_name,
        duration_minutes=test.duration_minutes,
        questions=question_data
    )

# ✅ 검사 시작 요청 스키마
class StartRequest(BaseModel):
    mode: str

# ✅ 검사 시작 응답 스키마
class StartResponse(BaseModel):
    message: str
    started_at: datetime

# ✅ 검사 시작 API
@router.post("/api/tests/{test_id}/start", response_model=StartResponse)
def start_test(test_id: str, request: StartRequest, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return StartResponse(message="Test session started.", started_at=datetime.utcnow())

# ✅ 응답 제출 요청 스키마
class AnswerSubmission(BaseModel):
    question_id: str
    selected_option_ids: List[str]

class SubmitRequest(BaseModel):
    email: str
    responses: List[AnswerSubmission]

# ✅ 응답 제출 응답 스키마
class SubmitResponse(BaseModel):
    message: str
    report_id: str

# ✅ 응답 제출 API 시작
@router.post("/api/tests/{test_id}/submit", response_model=SubmitResponse)
def submit_test(test_id: str, request: SubmitRequest, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    total_score = 0.0
    now = datetime.utcnow()
    year, month = now.year, now.month

    profile = db.query(UserProfile).filter(UserProfile.email == request.email).first()
    group_value = profile.school if profile else None

    for item in request.responses:
        question = db.query(Question).filter(
            Question.question_id == item.question_id,
            Question.test_id == test_id
        ).first()

        if not question:
            continue

        correct_option_ids = [
            opt.option_id for opt in db.query(Option).filter(
                Option.question_id == item.question_id,
                Option.is_correct == True
            ).all()
        ]

        is_correct = set(item.selected_option_ids) == set(correct_option_ids)
        if is_correct:
            total_score += 1

        response = Response(
            response_id=str(uuid.uuid4()),
            email=request.email,
            test_id=test_id,
            question_id=item.question_id,
            selected_option_ids=item.selected_option_ids,
            response_time_sec=0.0
        )
        db.add(response)

        if group_value:
            stat = db.query(QuestionStatsByGroup).filter_by(
                question_id=item.question_id,
                group_type=GroupTypeEnum.school,
                group_value=group_value,
                year=year,
                month=month
            ).first()

            if stat:
                previous_n = stat.num_responses
                stat.num_responses += 1
                stat.correct_rate = ((stat.correct_rate * previous_n) + (1 if is_correct else 0)) / stat.num_responses
                stat.avg_response_time = ((stat.avg_response_time * previous_n) + 0.0) / stat.num_responses

                dist = json.loads(stat.option_distribution_json or '{}')
                for opt_id in item.selected_option_ids:
                    dist[opt_id] = dist.get(opt_id, 0) + 1
                stat.option_distribution_json = json.dumps(dist)

            else:
                stat = QuestionStatsByGroup(
                    question_id=item.question_id,
                    group_type=GroupTypeEnum.school,
                    group_value=group_value,
                    year=year,
                    month=month,
                    num_responses=1,
                    correct_rate=1.0 if is_correct else 0.0,
                    avg_response_time=0.0,
                    option_distribution_json=json.dumps({
                        opt_id: 1 for opt_id in item.selected_option_ids
                    })
                )
                db.add(stat)

    score_standardized = total_score * 10

    sten_rule = db.query(STENRule).filter(
        STENRule.test_id == test_id,
        STENRule.min_score <= score_standardized,
        STENRule.max_score >= score_standardized
    ).first()

    score_level = f"STEN {sten_rule.sten_level}" if sten_rule else "STEN N/A"

    report = TestReport(
        report_id=str(uuid.uuid4()),
        email=request.email,
        test_id=test_id,
        score_total=total_score,
        score_standardized=score_standardized,
        score_level=score_level,
        result_summary="임시 요약"
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return SubmitResponse(
        message="Responses submitted successfully.",
        report_id=report.report_id
    )

# ✅ 검사 등록 요청 스키마
class CreateTestRequest(BaseModel):
    test_name: str
    test_type: TestTypeEnum
    version: str = "v1.0"
    version_note: str = ""
    duration_minutes: int = 30

# ✅ 검사 등록 응답 스키마
class CreateTestResponse(BaseModel):
    message: str
    test_id: str

# ✅ 검사 등록 API (super_admin만 가능하도록 수정)
@router.post("/api/tests", response_model=CreateTestResponse)
def create_test(
    request: CreateTestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ 관리자 인증 의존성 추가
):
    """
    ✅ 새로운 검사를 생성하는 API입니다.
    - 검사명, 유형, 버전 등을 받아서 DB에 저장합니다.
    - 📌 관리자(super_admin)만 생성 가능
    """
    if current_user.role != "super_admin":  # ✅ 권한 체크 로직 추가
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    new_test = Test(
        test_id=str(uuid.uuid4()),
        test_name=request.test_name,
        test_type=request.test_type,
        version=request.version,
        version_note=request.version_note,
        duration_minutes=request.duration_minutes,
        created_at=datetime.utcnow()
    )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return CreateTestResponse(
        message="검사가 성공적으로 등록되었습니다.",
        test_id=new_test.test_id
    )

# ✅ 사용자 전용 문항 조회 API
@router.get("/api/tests/{test_id}/questions-public", response_model=TestDetail)
def get_test_questions_for_user(test_id: str, db: Session = Depends(get_db)):
    """
    ✅ 사용자(응시자)용 문항 조회 API
    - 관리자 인증 없이 누구나 접근 가능
    - test_question_links 기준으로 순서대로 문항 + 선택지 반환
    """
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    # ✅ 연결된 문항 순서대로 불러오기
    from backend.models.test_question_links import TestQuestionLink
    links = (
        db.query(TestQuestionLink)
        .filter(TestQuestionLink.test_id == test_id)
        .order_by(TestQuestionLink.order_index.asc())
        .all()
    )
    question_ids = [link.question_id for link in links]

    questions = (
        db.query(Question)
        .filter(Question.question_id.in_(question_ids))
        .all()
    )

    question_map = {q.question_id: q for q in questions}

    # ✅ 문항 + 선택지 구성
    question_data = []
    for order, qid in enumerate(question_ids):
        q = question_map[qid]
        options = db.query(Option).filter(
            Option.question_id == q.question_id
        ).order_by(Option.option_order.asc()).all()

        question_data.append(QuestionSchema(
            question_id=q.question_id,
            question_text=q.question_text,
            question_type=q.question_type,
            is_multiple_choice=q.is_multiple_choice,
            order_index=order + 1,
            options=[
                OptionSchema(
                    option_id=o.option_id,
                    option_text=o.option_text,
                    option_order=o.option_order
                ) for o in options
            ]
        ))

    return TestDetail(
        test_id=test.test_id,
        test_name=test.test_name,
        duration_minutes=test.duration_minutes,
        questions=question_data
    )

# ✅ 검사 삭제 API
@router.delete("/api/tests/{test_id}")
def delete_test(
    test_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    ✅ 검사 삭제 API
    - 테스트 ID로 검사 삭제
    - 연결된 문항 연결 정보 먼저 삭제 필요 (FK 문제 방지)
    """
    from backend.models.test_question_links import TestQuestionLink
    from backend.models.test import Test

    # 🔧 연결된 문항 연결 정보 먼저 삭제
    db.query(TestQuestionLink).filter(TestQuestionLink.test_id == test_id).delete()

    # 🔧 실제 테스트 삭제
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    db.delete(test)
    db.commit()

    return {"message": "Test deleted successfully."}
