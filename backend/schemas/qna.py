# backend/schemas/qna.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ✅ 질문 등록 시 사용하는 기본 스키마
class QnABase(BaseModel):
    question: str                                      # 사용자 질문 내용
    is_private: Optional[bool] = False                 # 공개 여부 (기본값: 공개)

# ✅ 질문 생성 시 사용하는 스키마
class QnACreate(QnABase):
    pass  # 별도 필드 없음, QnABase 그대로 사용

# ✅ 관리자 답변 작성 시 사용하는 스키마
class QnAAnswer(BaseModel):
    answer: str  # 관리자 답변

# ✅ 전체 QnA 조회 시 출력용 스키마
class QnAOut(QnABase):
    id: str                                            # QnA 고유 ID (UUID)
    answer: Optional[str]                              # 관리자 답변 (없을 수 있음)
    created_by: Optional[str]                          # 작성자 UUID (nullable 허용)
    created_at: datetime                               # 질문 작성 시각
    answered_by: Optional[str]                         # 관리자 UUID (nullable 허용)
    answered_at: Optional[datetime]                    # 답변 작성 시각 (nullable 허용)

    class Config:
        orm_mode = True  # ✅ SQLAlchemy ORM 모델과의 자동 매핑 활성화
