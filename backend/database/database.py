# backend/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ config에서 안전하게 불러온 DB URL 사용
from backend.core.config import settings
DB_URL = settings.DATABASE_URL

# ✅ DB 엔진 생성
engine = create_engine(DB_URL, pool_pre_ping=True)

# ✅ 세션 로컬 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base 클래스 선언 (모든 모델이 이 클래스를 상속함)
Base = declarative_base()

# ✅ 의존성 주입용 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
