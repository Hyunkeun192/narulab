from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List, Any

from database import get_db
from models.scoring_rule import ScoringRule
from schemas.test_scoring_rule import (
    ScoringRuleCreateRequest,
    ScoringRuleUpdateRequest,
    ScoringRuleResponse,
)

# ✅ 관리자 인증 의존성 import
from dependencies.admin_auth import get_current_admin_user

# 관리자 채점 기준 라우터
router = APIRouter(
    prefix="/api/admin/scoring-rules",
    tags=["Admin - Scoring Rules"],
    dependencies=[Depends(get_current_admin_user)]  # ✅ 관리자 인증 적용
)

# ✅ 채점 기준 목록 조회
@router.get("/", response_model=List[ScoringRuleResponse])
def list_scoring_rules(db: Session = Depends(get_db)):
    return db.query(ScoringRule).order_by(ScoringRule.created_at.desc()).all()

# ✅ 채점 기준 등록
@router.post("/", response_model=ScoringRuleResponse)
def create_scoring_rule(
    request: ScoringRuleCreateRequest,
    db: Session = Depends(get_db)
):
    rule = ScoringRule(
        scoring_rule_id=uuid4(),
        test_id=request.test_id,
        scoring_key_name=request.scoring_key_name,
        scoring_type=request.scoring_type,
        is_objective=request.is_objective,
        scoring_stages=request.scoring_stages,
        scoring_logic_json=request.scoring_logic_json,
        norm_group_id=request.norm_group_id,
        description=request.description,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

# ✅ 채점 기준 수정
@router.put("/{scoring_rule_id}", response_model=ScoringRuleResponse)
def update_scoring_rule(
    scoring_rule_id: UUID,
    request: ScoringRuleUpdateRequest,
    db: Session = Depends(get_db)
):
    rule = db.query(ScoringRule).filter(ScoringRule.scoring_rule_id == scoring_rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Scoring rule not found.")

    for field, value in request.dict(exclude_unset=True).items():
        setattr(rule, field, value)

    db.commit()
    db.refresh(rule)
    return rule

# ✅ 채점 기준 삭제 (미사용 조건 시만)
@router.delete("/{scoring_rule_id}")
def delete_scoring_rule(
    scoring_rule_id: UUID,
    db: Session = Depends(get_db)
):
    rule = db.query(ScoringRule).filter(ScoringRule.scoring_rule_id == scoring_rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Scoring rule not found.")

    db.delete(rule)
    db.commit()
    return {"message": "Scoring rule deleted."}
