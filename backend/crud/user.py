from sqlalchemy.orm import Session
from backend.models.user import User, UserProfile
from backend.schemas.user import UserCreate
from backend.core.security import hash_password
import uuid

# ✅ 암호화된 이메일로 사용자 조회
# ✅ 수정 완료: 이미 암호화된 이메일을 받아 그대로 조회
def get_user_by_email(db: Session, encrypted_email: str):
    """
    로그인 시 이미 암호화된 이메일 값을 기준으로 사용자 조회
    - 중복 암호화를 방지하기 위해 aes_encrypt 제거
    """
    return db.query(User).filter(User.encrypted_email == encrypted_email).first()

# ✅ 전화번호로 사용자 조회
def get_user_by_phone(db: Session, encrypted_phone: str):
    return db.query(User).filter(User.encrypted_phone_number == encrypted_phone).first()

# ✅ 사용자 생성 함수
def create_user(db: Session, user_data: UserCreate, encrypted_email: str, encrypted_phone: str):
    """
    신규 사용자 생성 함수
    - 이메일/전화번호는 암호화되어 전달됨
    - 비밀번호는 bcrypt 해시
    """
    user = User(
        user_id=str(uuid.uuid4()),
        encrypted_email=encrypted_email,
        encrypted_phone_number=encrypted_phone,
        nickname=user_data.nickname,
        hashed_password=hash_password(user_data.password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ✅ 사용자 프로필 생성
def create_user_profile(db: Session, user_id: str, email: str):
    """
    이메일은 평문 그대로 저장 (user_profiles 테이블용)
    """
    profile = UserProfile(
        email=email,
        user_id=user_id,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

# ✅ 닉네임 중복 여부 확인
def get_user_by_nickname(db: Session, nickname: str):
    """
    닉네임 중복 여부 확인
    """
    return db.query(User).filter(User.nickname == nickname).first()
