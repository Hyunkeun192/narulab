# schemas/notice.py
from pydantic import BaseModel
from datetime import datetime

class NoticeBase(BaseModel):
    title: str
    content: str

class NoticeCreate(NoticeBase):
    pass

class NoticeOut(NoticeBase):
    id: int
    created_at: datetime
    created_by: int

    class Config:
        orm_mode = True