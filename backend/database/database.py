from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ✅ 환경 변수에서 DB URL을 불러옴
DB_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/mydatabase")

# ❌ 보안상 위험한 출력 제거됨
# print(DB_URL)  # 🔒 운영 환경에서 DB 정보 노출 위험 → 삭제함

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
