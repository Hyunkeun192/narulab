from sqlalchemy import Column, String, Float, Integer, Enum, ForeignKey, Text
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

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # UUID → String
    question_id = Column(String(36), ForeignKey("questions.question_id"), nullable=False)  # UUID → String

    group_type = Column(Enum(GroupTypeEnum), nullable=False)
    group_value = Column(String(100))  # 길이 명시

    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)

    num_responses = Column(Integer, nullable=True)
    correct_rate = Column(Float, nullable=True)
    avg_response_time = Column(Float, nullable=True)
    option_distribution_json = Column(Text, nullable=True)  # JSON 문자열로 저장
