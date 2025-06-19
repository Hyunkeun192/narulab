# backend/models/qna.py

from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.database import Base

class QnA(Base):
    __tablename__ = "qna"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # ✅ UUID 기반 PK

    title = Column(String(200), nullable=False)       # ✅ 질문 제목
    content = Column(Text, nullable=False)            # ✅ 질문 본문
    answer = Column(Text, nullable=True)              # ✅ 관리자 답변
    is_private = Column(Boolean, default=False)       # ✅ 비공개 여부

    # 🔧 수정됨: 외래키 타입과 참조 경로를 users.user_id 기준으로 변경
    created_by = Column(String(36), ForeignKey("users.user_id"))   # ✅ 질문 작성자
    answered_by = Column(String(36), ForeignKey("users.user_id"))  # ✅ 답변 작성자

    # ✅ 관계 설정 (작성자, 답변자 모두 User 테이블과 연결)
    created_user = relationship("User", foreign_keys=[created_by], backref="qnas_created")
    answered_user = relationship("User", foreign_keys=[answered_by], backref="qnas_answered")
