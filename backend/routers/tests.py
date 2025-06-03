# app/routers/tests.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
# ✅ Report → TestReport로 이름 변경하여 중복 오류 해결
from backend.models.test import Test, Question, Option, Response, TestReport
from backend.models.test_analytics_by_group import TestAnalyticsByGroup, GroupTypeEnum
from backend.models.question_stats_by_group import QuestionStatsByGroup
from backend.models.sten_rule import STENRule  # ✅ STEN 등급 규칙 모델 import
from backend.models.user import UserProfile  # ✅ 사용자 프로필 (school 등)
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
        orm_mode = True

# ✅ 선택지 응답용 스키마
class OptionSchema(BaseModel):
    option_id: str
    option_text: str
    option_order: int

    class Config:
        orm_mode = True

# ✅ 문항 응답용 스키마
class QuestionSchema(BaseModel):
    question_id: str
    question_text: str
    question_type: str
    is_multiple_choice: bool
    order_index: int
    options: List[OptionSchema]

    class Config:
        orm_mode = True

# ✅ 검사 상세 조회용 스키마
class TestDetail(BaseModel):
    test_id: str
    test_name: str
    duration_minutes: int
    questions: List[QuestionSchema]

    class Config:
        orm_mode = True

# ✅ 전체 검사 목록 조회
@router.get("/api/tests", response_model=List[TestSummary])
def get_tests(db: Session = Depends(get_db)):
    tests = db.query(Test).order_by(Test.created_at.desc()).all()
    return tests

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

    # ✅ 사용자 프로필 조회 (school 기준 그룹 통계용)
    profile = db.query(UserProfile).filter(UserProfile.email == request.email).first()
    group_value = profile.school if profile else None

    # ✅ 문항 응답 순회 및 채점 처리
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

        # ✅ 응답 저장
        response = Response(
            response_id=str(uuid.uuid4()),
            email=request.email,
            test_id=test_id,
            question_id=item.question_id,
            selected_option_ids=item.selected_option_ids,
            response_time_sec=0.0  # TODO: 측정 기능 적용 예정
        )
        db.add(response)

        # ✅ 문항별 그룹 통계 자동 집계 (school 기준)
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

                # ✅ 선택지 분포 업데이트
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

    # ✅ STEN 등급 계산 로직 (score_standardized → score_level)
    score_standardized = total_score * 10

    sten_rule = db.query(STENRule).filter(
        STENRule.test_id == test_id,
        STENRule.min_score <= score_standardized,
        STENRule.max_score >= score_standardized
    ).first()

    score_level = f"STEN {sten_rule.sten_level}" if sten_rule else "STEN N/A"

    # ✅ 리포트 저장 (TestReport로 클래스 이름 변경됨)
    report = TestReport(  # ✅ Report → TestReport 이름 변경
        report_id=str(uuid.uuid4()),
        email=request.email,
        test_id=test_id,
        score_total=total_score,
        score_standardized=score_standardized,
        score_level=score_level,
        result_summary="임시 요약"
    )
    db.add(report)

    # ✅ 커밋 및 응답
    db.commit()
    db.refresh(report)

    return SubmitResponse(
        message="Responses submitted successfully.",
        report_id=report.report_id
    )

