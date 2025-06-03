# backend/routers/admin_norms.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.dependencies.external_admin_auth import get_super_admin_user

# ✅ 슈퍼 관리자 인증 필요
router = APIRouter(
    prefix="/api/admin/norms",
    tags=["Admin - Norms"],
    dependencies=[Depends(get_super_admin_user)]
)

# ✅ 규준 목록 조회 Mock API
@router.get("")
def get_all_norms(db: Session = Depends(get_db)):
    """
    현재는 빈 목록을 반환하는 Mock API입니다.
    향후 규준 그룹 및 STEN 규칙 데이터를 반환하도록 확장 가능합니다.
    """
    return []  # ✅ 현재는 빈 배열 반환 (프론트엔드 404 방지용)
