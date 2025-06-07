# backend/routers/admin_upload.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from backend.database.database import get_db
from backend.dependencies.external_admin_auth import get_super_admin_user
from sqlalchemy.orm import Session
import boto3
import uuid
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ .env 파일에서 환경변수 로드

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_BASE_URL = os.getenv("S3_BASE_URL")

router = APIRouter(
    prefix="/api/admin/questions",
    tags=["Admin - Upload"],
    dependencies=[Depends(get_super_admin_user)]
)

@router.post("/upload-image")
async def upload_image_to_s3(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 파일 확장자 체크
    filename = file.filename
    ext = filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
        raise HTTPException(status_code=400, detail="허용되지 않은 이미지 형식입니다.")

    # 고유한 S3 객체 키 생성
    key = f"questions/images/{uuid.uuid4()}.{ext}"

    # boto3 클라이언트 설정
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    try:
        # S3에 파일 업로드
        s3.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            key,
            ExtraArgs={"ContentType": file.content_type, "ACL": "public-read"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 업로드 실패: {str(e)}")

    # 최종 URL 반환
    image_url = f"{S3_BASE_URL}{key}"
    return {"image_url": image_url}
