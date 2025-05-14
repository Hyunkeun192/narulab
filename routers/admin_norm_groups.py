from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List

from app.database import get_db
from app.models.norm_group import NormGroup
from app.schemas.test_norm_group import (
    NormGroupCreateRequest,
    NormGroupUpdateRequest,
    NormGroupResponse,
)

# ✅ 관리자 인증 의존성 import
from app.dependencies.admin_auth import get_current_admin_user

# 관리자 규준 관리 라우터
router = APIRouter(
    prefix="/api/admin/norm-groups",
    tags=["Admin - Norm Groups"],
    dependencies=[Depends(get_current_admin_user)]  # ✅ 관리자 인증 적용
)

# ✅ 규준 목록 조회
@router.get("/", response_model=List[NormGroupResponse])
def list_norm_groups(db: Session = Depends(get_db)):
    return db.query(NormGroup).order_by(NormGroup.created_at.desc()).all()

# ✅ 규준 등록
@router.post("/", response_model=NormGroupResponse)
def create_norm_group(
    request: NormGroupCreateRequest,
    db: Session = Depends(get_db)
):
    group = NormGroup(
        norm_group_id=uuid4(),
        norm_name=request.norm_name,
        mean=request.mean,
        stddev=request.stddev,
        level_mapping_json=request.level_mapping_json,
        description=request.description
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

# ✅ 규준 수정
@router.put("/{norm_group_id}", response_model=NormGroupResponse)
def update_norm_group(
    norm_group_id: UUID,
    request: NormGroupUpdateRequest,
    db: Session = Depends(get_db)
):
    group = db.query(NormGroup).filter(NormGroup.norm_group_id == norm_group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Norm group not found.")

    for field, value in request.dict(exclude_unset=True).items():
        setattr(group, field, value)

    db.commit()
    db.refresh(group)
    return group

# ✅ 규준 삭제
@router.delete("/{norm_group_id}")
def delete_norm_group(
    norm_group_id: UUID,
    db: Session = Depends(get_db)
):
    group = db.query(NormGroup).filter(NormGroup.norm_group_id == norm_group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Norm group not found.")

    db.delete(group)
    db.commit()
    return {"message": "Norm group deleted."}
