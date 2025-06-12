# backend/utils/init_db.py
from backend.database.database import Base, engine
from backend.models import user, qna  # 필요한 모든 모델 import

print("⏳ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created.")
