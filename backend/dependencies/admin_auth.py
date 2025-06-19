from backend.database.database import get_db  # ✅ SessionLocal → get_db 수정
# app/dependencies/admin_auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from backend.database.database import SessionLocal
from backend.models.user import User

from backend.core.config import settings  # ✅ 설정 파일에서 불러오도록 수정

# ✅ JWT 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
SECRET_KEY = settings.JWT_SECRET_KEY  # ✅ token.py와 동일한 키로 통일
ALGORITHM = settings.JWT_ALGORITHM    # ✅ 알고리즘도 설정과 통일

# ✅ 현재 로그인된 사용자 반환
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ✅ 관리자 인증 의존성 (방법 1 적용)
def get_current_admin_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in ("super_admin", "content_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다."
        )
    return current_user

# ✅ 슈퍼 관리자 전용 인증
def get_super_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="슈퍼 관리자만 접근할 수 있습니다.")
    return current_user

# ✅ 🔧 super_admin 또는 content_admin 권한 허용
def get_content_or_super_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in ("super_admin", "content_admin"):
        raise HTTPException(
            status_code=403,
            detail="접근 권한이 없습니다 (super_admin 또는 content_admin만 가능)"
        )
    return current_user