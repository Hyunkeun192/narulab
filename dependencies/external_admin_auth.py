from database.database import get_db  # ✅ SessionLocal → get_db 수정
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.institution_admin import InstitutionAdmin
from models.user import User
from dependencies.admin_auth import get_current_user

# ✅ 학교 관리자 인증
def get_school_admin_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> InstitutionAdmin:
    admin = db.query(InstitutionAdmin).filter(
        InstitutionAdmin.user_id == current_user.user_id,
        InstitutionAdmin.institution_type == "school",
        InstitutionAdmin.approved == True
    ).first()
    if not admin:
        raise HTTPException(status_code=403, detail="학교 관리자 권한이 없습니다.")
    return admin

# ✅ 기업 관리자 인증
def get_company_admin_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> InstitutionAdmin:
    admin = db.query(InstitutionAdmin).filter(
        InstitutionAdmin.user_id == current_user.user_id,
        InstitutionAdmin.institution_type == "company",
        InstitutionAdmin.approved == True
    ).first()
    if not admin:
        raise HTTPException(status_code=403, detail="기업 관리자 권한이 없습니다.")
    return admin
