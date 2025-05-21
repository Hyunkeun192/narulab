from sqlalchemy import Column, String, Float, Integer, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from backend.database.database import Base
from uuid import uuid4
import enum

# ✅ 그룹 유형 enum 재사용
class GroupTypeEnum(str, enum.Enum):
    school = "school"
    region = "region"
    company = "company"
    age = "age"

# ✅ 문항별 그룹 통계 테이블
class QuestionStatsByGroup(Base):
    __tablename__ = "question_stats_by_group"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False)

    group_type = Column(Enum(GroupTypeEnum), nullable=False)
    group_value = Column(String, nullable=False)

    year = Column(Integer, nullable=True)   # ✅ 연도 기준 필터용
    month = Column(Integer, nullable=True)  # ✅ 월 기준 필터용

    num_responses = Column(Integer, nullable=True)
    correct_rate = Column(Float, nullable=True)
    avg_response_time = Column(Float, nullable=True)
    option_distribution_json = Column(String, nullable=True)  # JSON 문자열로 저장
