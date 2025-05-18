# app/routers/verification.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
from models.verification_code import VerificationCode
from schemas.verification import VerificationRequest, VerificationConfirm
import random
from datetime import datetime, timedelta

router = APIRouter()

# ✅ 인증번호 요청 API
@router.post("/api/verify/request")
def request_verification(data: VerificationRequest, db: Session = Depends(get_db)):
    # 1. 인증코드 생성
    code = str(random.randint(10000, 99999))

    # 2. 기존 코드 삭제
    db.query(VerificationCode).filter(
        VerificationCode.target == data.target,
        VerificationCode.type == data.type
    ).delete()

    # 3. 새 코드 저장
    verification = VerificationCode(
        target=data.target,
        type=data.type,
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )
    db.add(verification)
    db.commit()

    # 4. 인증번호 전송 (실제 구현 필요)
    if data.type == "email":
        print(f"[이메일 전송] {data.target} → 인증번호: {code}")  # TODO: 이메일 전송 함수 연결
    else:
        print(f"[문자 전송] {data.target} → 인증번호: {code}")  # TODO: 문자 전송 API 연동

    return {"message": "Verification code sent."}

# ✅ 인증번호 확인 API
@router.post("/api/verify/confirm")
def confirm_verification(data: VerificationConfirm, db: Session = Depends(get_db)):
    record = db.query(VerificationCode).filter(
        VerificationCode.target == data.target,
        VerificationCode.type == data.type,
        VerificationCode.code == data.code
    ).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid verification code.")

    if record.is_expired():
        raise HTTPException(status_code=400, detail="Verification code has expired.")

    # ✅ 확인 완료 → 인증된 사용자 처리 (추후 활용)
    return {"message": "Verification successful."}
