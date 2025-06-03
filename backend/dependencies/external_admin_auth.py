from backend.database.database import get_db  # ✅ SessionLocal → get_db 수정
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal
from backend.models.institution_admin import InstitutionAdmin
from backend.models.user import User
from backend.dependencies.admin_auth import get_current_user

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

# ✅ 콘텐츠 관리자 인증
def get_content_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    콘텐츠 관리자 권한 확인 함수
    - 조건: 사용자 role 이 "content" 인 경우 통과
    """
    if current_user.role != "content":
        raise HTTPException(status_code=403, detail="콘텐츠 관리자만 접근할 수 있습니다.")
    return current_user

# ✅ 슈퍼 관리자 인증 (추가됨)
def get_super_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    슈퍼 관리자 권한 확인 함수
    - 조건: 사용자 role 이 "super_admin" 인 경우 통과
    """
    if current_user.role != "super_admin":
        raise HTTPException(status_code=403, detail="슈퍼 관리자만 접근할 수 있습니다.")
    return current_user
