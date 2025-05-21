# narulab/routers/admin_sten_rule.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models.sten_rule import STENRule
from backend.schemas.sten_rule import STENRuleCreate, STENRuleUpdate, STENRuleOut
from backend.dependencies.admin_auth import get_current_super_admin
from backend.dependencies.content_admin_auth import get_current_content_admin
from typing import List, Union

router = APIRouter(
    prefix="/api/admin/sten-rules",
    tags=["Admin - STEN Rule"],
    dependencies=[Depends(lambda: get_current_super_admin() or get_current_content_admin())]
)

# ✅ 특정 검사에 대한 STEN 규칙 목록 조회
@router.get("/{test_id}", response_model=List[STENRuleOut])
def list_sten_rules(test_id: str, db: Session = Depends(get_db)):
    return db.query(STENRule).filter(STENRule.test_id == test_id).order_by(STENRule.sten_level).all()

# ✅ STEN 규칙 등록
@router.post("/", response_model=STENRuleOut)
def create_sten_rule(rule: STENRuleCreate, db: Session = Depends(get_db)):
    db_rule = STENRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

# ✅ STEN 규칙 수정
@router.put("/{rule_id}", response_model=STENRuleOut)
def update_sten_rule(rule_id: int, rule: STENRuleUpdate, db: Session = Depends(get_db)):
    db_rule = db.query(STENRule).filter(STENRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="STEN rule not found")
    for key, value in rule.dict().items():
        setattr(db_rule, key, value)
    db.commit()
    db.refresh(db_rule)
    return db_rule

# ✅ STEN 규칙 삭제
@router.delete("/{rule_id}")
def delete_sten_rule(rule_id: int, db: Session = Depends(get_db)):
    db_rule = db.query(STENRule).filter(STENRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="STEN rule not found")
    db.delete(db_rule)
    db.commit()
    return {"message": "STEN rule deleted"}
