from pydantic import BaseModel
from typing import List, Any
from uuid import UUID

# 🔸 문항 제거 요청 스키마
class RemoveQuestionRequest(BaseModel):
    question_ids: List[UUID]  # 제거할 문항 ID 목록

# 🔸 응답 스키마
class RemoveQuestionResponse(BaseModel):
    removed_count: int        # 제거된 문항 수
    message: str              # 결과 메시지
