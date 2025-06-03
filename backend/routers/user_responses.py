# backend/routers/user_responses.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from backend.database.database import get_db  # ✅ 수정된 get_db 경로
from backend.schemas.response import ResponseSubmit, ReportResult  # ✅ 수정된 스키마 import
# ✅ Report → UserReport로 클래스명 변경
from backend.models.response import UserReport  # ✅ 결과 리포트 저장용 모델
from backend.models.test import Test
from backend.models.option import Option
from backend.models.norm_group import NormGroup  # ✅ 규준 그룹 정보
from backend.models.report_rule import ReportRule  # ✅ STEN 해석 문구
from datetime import datetime

router = APIRouter(
    prefix="/api/user",
    tags=["user-responses"]
)

# ✅ 사용자 응답 제출 → 점수 계산 → STEN 등급 추정 → 리포트 생성 및 반환
@router.post("/responses", response_model=ReportResult)
def submit_response(payload: ResponseSubmit, db: Session = Depends(get_db)):
    # ✅ 1. 점수 계산
    total_questions = len(payload.answers)
    if total_questions == 0:
        raise HTTPException(status_code=400, detail="문항 응답이 없습니다.")

    correct_count = 0

    for answer in payload.answers:
        correct_options = db.query(Option).filter(
            Option.question_id == answer.question_id,
            Option.is_correct == True
        ).all()

        correct_ids = {str(opt.option_id) for opt in correct_options}
        selected_ids = {str(opt_id) for opt_id in answer.selected_option_ids}

        if correct_ids == selected_ids:
            correct_count += 1

    raw_score = int((correct_count / total_questions) * 100)

    # ✅ 2. 규준(STEN) 추정
    norm = db.query(NormGroup).filter(NormGroup.test_id == payload.test_id).first()
    if not norm or not norm.rules:
        raise HTTPException(status_code=400, detail="해당 검사에 규준 정보가 없습니다.")

    matched = None
    for rule in norm.rules:  # rules는 JSON 리스트로 가정
        if rule["min_score"] <= raw_score <= rule["max_score"]:
            matched = rule
            break

    if not matched:
        raise HTTPException(status_code=400, detail="STEN 계산 실패")

    sten = matched["sten"]

    # ✅ 3. 리포트 해석 문구 추출
    rule_obj = db.query(ReportRule).filter(ReportRule.test_id == payload.test_id).first()
    if not rule_obj:
        raise HTTPException(status_code=400, detail="리포트 기준 없음")

    description = rule_obj.sten_descriptions.get(str(sten), "해석 정보 없음")

    # ✅ 4. 리포트 저장
    report = UserReport(  # ✅ Report → UserReport 이름 변경
        user_id=payload.user_id,
        test_id=payload.test_id,
        score=raw_score,
        sten=sten,
        description=description,
        created_at=datetime.now().isoformat()
    )
    db.add(report)
    db.commit()

    return {
        "score": raw_score,
        "sten": sten,
        "description": description,
    }
