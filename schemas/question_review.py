from pydantic import BaseModel
from typing import Optional

# 🔸 문항 검토 요청 스키마
class QuestionReviewRequest(BaseModel):
    approved: bool                      # True → 승인 / False → 반려
    review_comment: Optional[str] = None  # 반려 사유 (반려일 경우에만 사용)

# 🔸 문항 검토 응답 스키마
class QuestionReviewResponse(BaseModel):
    message: str                        # 처리 결과 메시지 ("approved", "rejected")
