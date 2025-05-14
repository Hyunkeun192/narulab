# app/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# SQLAlchemy 연결 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# 세션 로컬 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 (모든 모델이 이걸 상속)
Base = declarative_base()
