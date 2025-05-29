from pydantic import BaseModel
from datetime import datetime

class NoticeBase(BaseModel):
    title: str
    content: str

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(NoticeBase):
    pass

class NoticeOut(NoticeBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True
