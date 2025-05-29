from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QnABase(BaseModel):
    question: str

class QnACreate(QnABase):
    pass

class QnAAnswer(BaseModel):
    answer: str

class QnAOut(QnABase):
    id: str
    answer: Optional[str]
    created_by: str
    created_at: datetime
    answered_by: Optional[str]
    answered_at: Optional[datetime]

    class Config:
        orm_mode = True
