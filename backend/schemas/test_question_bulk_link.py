from pydantic import BaseModel
from typing import List
from uuid import UUID

class TestQuestionBulkLinkRequest(BaseModel):
    question_ids: List[UUID]
