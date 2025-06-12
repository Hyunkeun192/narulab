# backend/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from backend.core.config import settings

# ✅ DATABASE_URL이 반드시 존재해야 하므로 명시적으로 확인
assert settings.DATABASE_URL is not None, "❌ DATABASE_URL 환경변수가 설정되지 않았습니다."

# ✅ 디버깅용 출력 (실행 후 제거 가능)
print("✅ Loaded DATABASE_URL:", settings.DATABASE_URL)

# SQLAlchemy 연결 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# 세션 로컬 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 (모든 모델이 이걸 상속)
Base = declarative_base()

# ✅ get_db 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
