from pydantic import BaseModel
from typing import List
from uuid import UUID

# 🔸 문항 추가 요청 스키마
class AddQuestionRequest(BaseModel):
    question_ids: List[UUID]  # 연결할 문항 ID 목록

# 🔸 응답 스키마
class AddQuestionResponse(BaseModel):
    added_count: int          # 실제 추가된 문항 수
    message: str              # 결과 메시지
