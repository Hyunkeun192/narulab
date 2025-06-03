# backend/schemas/report.py

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# ✅ 리포트 응답용 출력 스키마
class ReportOut(BaseModel):
    report_id: UUID
    user_id: UUID
    test_id: UUID
    score: int
    sten: int
    description: str
    created_at: str

    class Config:
        orm_mode = True
