# backend/core/config.py

import os
from dotenv import load_dotenv
from pathlib import Path

# ✅ 절대경로 기반으로 .env 로드 (운영/개발 모두 안전)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /Users/hyunkeunkim/Desktop/narulab
env_name = os.getenv("ENV", "development")
env_file = BASE_DIR / (".env.production" if env_name == "production" else ".env")

load_dotenv(dotenv_path=env_file)  # ✅ 명시적으로 절대경로 지정

class Settings:
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    AES_SECRET_KEY: str = os.getenv("AES_SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
