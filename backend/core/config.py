# app/core/config.py

import os
from dotenv import load_dotenv

# ✅ 개발/운영 환경 구분
# ENV 환경변수가 'production'이면 .env.production, 아니면 .env 사용
env_name = os.getenv("ENV", "development")
env_file = ".env.production" if env_name == "production" else ".env"

load_dotenv(dotenv_path=env_file)


class Settings:
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    AES_SECRET_KEY: str = os.getenv("AES_SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # ✅ 기본값 추가
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # ✅ 추가

    


settings = Settings()
