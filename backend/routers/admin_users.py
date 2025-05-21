# app/routers/admin_users.py

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_

from backend.database.database import get_db
from backend.models.user import User
from backend.schemas.user_admin import UserListItem, AdminRoleUpdateRequest  # ✅ 역할 변경 요청 스키마 포함
from backend.dependencies.admin_auth import get_current_admin_user  # ✅ 인증 의존성 (슈퍼 관리자 포함)

# 관리자 사용자 관리 라우터
router = APIRouter(
    prefix="/api/admin/users",
    tags=["Admin - Users"],
    dependencies=[Depends(get_current_admin_user)]
)

# ✅ 사용자 목록 조회 + 필터 검색 API
@router.get("/", response_model=List[UserListItem])
def get_user_list(
    keyword: Optional[str] = Query(None, description="닉네임 또는 이메일 검색"),
    is_active: Optional[bool] = Query(None, description="활성화 여부 필터"),
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if keyword:
        query = query.filter(
            or_(
                User.nickname.ilike(f"%{keyword}%"),
                User.encrypted_email.ilike(f"%{keyword}%")
            )
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.order_by(User.created_at.desc()).all()

# ❌ 사용하지 않는 관리자 생성 API는 현재 스키마 없음으로 인해 주석 처리
"""
@router.post("/")
def create_admin_user(
    request: AdminUserCreateRequest,
    db: Session = Depends(get_db)
):
    # 이메일 중복 확인
    existing = db.query(User).filter(User.encrypted_email == request.encrypted_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="해당 이메일로 등록된 사용자가 이미 존재합니다.")

    new_admin = User(
        encrypted_email=request.encrypted_email,
        encrypted_phone_number=request.encrypted_phone_number,
        nickname=request.nickname,
        hashed_password=request.hashed_password,
        is_admin=True  # ✅ 관리자 권한 설정
    )
    db.add(new_admin)
    db.commit()

    return {"message": "관리자 계정이 생성되었습니다."}
"""

# ✅ 관리자 계정 비활성화 API
@router.delete("/{user_id}")
def deactivate_admin_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    if not user.is_admin:
        raise HTTPException(status_code=400, detail="해당 사용자는 관리자 계정이 아닙니다.")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="이미 비활성화된 계정입니다.")

    user.is_active = False
    db.commit()

    return {"message": f"관리자 계정이 비활성화되었습니다: {user.nickname}"}

# ✅ 관리자 역할 변경 API (슈퍼 관리자만 수행 가능)
@router.put("/{user_id}/role")
def update_admin_role(
    user_id: str,
    request: AdminRoleUpdateRequest,  # {"role": "manager"} 또는 "viewer", "super"
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    # ✅ 현재 요청자가 슈퍼 관리자인지 확인
    if current_admin.role != "super":
        raise HTTPException(status_code=403, detail="슈퍼 관리자만 역할 변경이 가능합니다.")

    # ✅ 대상 사용자 조회
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    if not user.is_admin:
        raise HTTPException(status_code=400, detail="해당 사용자는 관리자 계정이 아닙니다.")

    # ✅ 역할 변경
    user.role = request.role
    db.commit()

    return {"message": f"{user.nickname}의 역할이 {request.role}로 변경되었습니다."}
