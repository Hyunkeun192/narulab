# app/routers/admin_external_admins.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from database.database import get_db
from models.institution_admin import InstitutionAdmin
from models.user import User
from dependencies.admin_auth import get_super_admin_user
from schemas.external_admin import (
    ExternalAdminCreateRequest,
    ExternalAdminApprovalRequest
)

router = APIRouter(
    prefix="/api/admin/external-admins",
    tags=["Admin - External Admins"],
    dependencies=[Depends(get_super_admin_user)]  # ✅ 슈퍼 관리자 전용
)

# ✅ 외부 관리자 등록 요청 생성
@router.post("/")
def create_external_admin(
    request: ExternalAdminCreateRequest,
    db: Session = Depends(get_db)
):
    # 중복 검사
    exists = db.query(InstitutionAdmin).filter(
        InstitutionAdmin.user_id == request.user_id,
        InstitutionAdmin.institution_type == request.institution_type,
        InstitutionAdmin.institution_name == request.institution_name
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="이미 등록된 요청입니다.")

    user = db.query(User).filter(User.user_id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    admin = InstitutionAdmin(
        admin_id=str(uuid4()),
        user_id=request.user_id,
        institution_type=request.institution_type,
        institution_name=request.institution_name,
        approved=False
    )
    db.add(admin)
    db.commit()
    return {"message": "외부 관리자 요청이 생성되었습니다."}

# ✅ 외부 관리자 승인/거절
@router.put("/{admin_id}/approve")
def approve_external_admin(
    admin_id: str,
    request: ExternalAdminApprovalRequest,
    db: Session = Depends(get_db)
):
    admin = db.query(InstitutionAdmin).filter(
        InstitutionAdmin.admin_id == admin_id
    ).first()
    if not admin:
        raise HTTPException(status_code=404, detail="관리자 요청을 찾을 수 없습니다.")

    admin.approved = request.approved
    db.commit()

    status_msg = "승인됨" if request.approved else "거절됨"
    return {"message": f"외부 관리자 요청이 {status_msg} 처리되었습니다."}
