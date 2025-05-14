from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.question import QuestionStatus

# 🔸 문항 목록 출력용 스키마
class QuestionListItem(BaseModel):
    question_id: UUID                        # 문항 고유 ID
    test_id: UUID                            # 소속된 검사 ID
    question_text: str                       # 질문 텍스트
    question_type: str                       # 문항 유형 (text, image 등)
    is_multiple_choice: bool                 # 복수 선택 여부
    status: QuestionStatus                   # 문항 상태 (waiting, approved, rejected)
    created_at: datetime                     # 생성일시

    class Config:
        orm_mode = True                      # SQLAlchemy ORM 객체 직렬화 허용
