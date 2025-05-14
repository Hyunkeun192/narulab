# app/routers/tests.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.test import Test, Question, Option, Response, Report
from typing import List
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import uuid

router = APIRouter()


# ✅ DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ 검사 유형 enum
class TestTypeEnum(str, Enum):
    aptitude = "aptitude"
    personality = "personality"


# ✅ 검사 목록 응답 스키마
class TestSummary(BaseModel):
    test_id: str
    test_name: str
    test_type: TestTypeEnum
    duration_minutes: int
    version: str

    class Config:
        orm_mode = True


# ✅ 선택지 스키마
class OptionSchema(BaseModel):
    option_id: str
    option_text: str
    option_order: int

    class Config:
        orm_mode = True


# ✅ 문항 스키마
class QuestionSchema(BaseModel):
    question_id: str
    question_text: str
    question_type: str
    is_multiple_choice: bool
    order_index: int
    options: List[OptionSchema]

    class Config:
        orm_mode = True


# ✅ 검사 상세 스키마
class TestDetail(BaseModel):
    test_id: str
    test_name: str
    duration_minutes: int
    questions: List[QuestionSchema]

    class Config:
        orm_mode = True


# ✅ 검사 목록 조회
@router.get("/api/tests", response_model=List[TestSummary])
def get_tests(db: Session = Depends(get_db)):
    tests = db.query(Test).order_by(Test.created_at.desc()).all()
    return tests


# ✅ 검사 상세 조회
@router.get("/api/tests/{test_id}", response_model=TestDetail)
def get_test_detail(test_id: str, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


# ✅ 검사 시작
class StartRequest(BaseModel):
    mode: str

class StartResponse(BaseModel):
    message: str
    started_at: datetime

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
    email: str  # 암호화된 이메일
    responses: List[AnswerSubmission]


# ✅ 응답 제출 응답 스키마
class SubmitResponse(BaseModel):
    message: str
    report_id: str


# ✅ 검사 응답 제출 API
@router.post("/api/tests/{test_id}/submit", response_model=SubmitResponse)
def submit_test(test_id: str, request: SubmitRequest, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    total_score = 0.0
    for item in request.responses:
        question = db.query(Question).filter(
            Question.question_id == item.question_id,
            Question.test_id == test_id
        ).first()

        if not question:
            continue

        # 정답 옵션 목록
        correct_option_ids = [
            opt.option_id for opt in db.query(Option).filter(
                Option.question_id == item.question_id,
                Option.is_correct == True
            ).all()
        ]

        # 정답 비교 (단순 정확 일치 기준)
        if set(item.selected_option_ids) == set(correct_option_ids):
            total_score += 1

        # 응답 저장
        response = Response(
            response_id=str(uuid.uuid4()),
            email=request.email,
            test_id=test_id,
            question_id=item.question_id,
            selected_option_ids=item.selected_option_ids,
            response_time_sec=0.0  # TODO: 응답 시간 추후 반영
        )
        db.add(response)

    # 리포트 저장
    report = Report(
        report_id=str(uuid.uuid4()),
        email=request.email,
        test_id=test_id,
        score_total=total_score,
        score_standardized=total_score * 10,  # 임시 변환 로직
        score_level="STEN 7",  # TODO: 나중에 규준 기반 계산
        result_summary="임시 요약",  # TODO: GPT 기반 요약 예정
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return SubmitResponse(
        message="Responses submitted successfully.",
        report_id=report.report_id
    )
