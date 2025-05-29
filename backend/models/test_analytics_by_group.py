from sqlalchemy import Column, String, Float, Enum, ForeignKey, Integer, Text
from backend.database.database import Base
from uuid import uuid4
import enum

# ✅ 그룹 유형 enum 정의
class GroupTypeEnum(str, enum.Enum):
    school = "school"
    region = "region"
    company = "company"
    age = "age"

# ✅ 검사별 그룹 통계 테이블
class TestAnalyticsByGroup(Base):
    __tablename__ = "test_analytics_by_group"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # ✅ UUID → String
    test_id = Column(String(36), ForeignKey("tests.test_id"), nullable=False)  # ✅ UUID → String

    group_type = Column(Enum(GroupTypeEnum), nullable=False)
    group_value = Column(String(100))  # ✅ 길이 명시

    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)

    avg_total_score = Column(Float, nullable=True)
    std_total_score = Column(Float, nullable=True)
    completion_rate = Column(Float, nullable=True)
    overall_correct_rate = Column(Float, nullable=True)

    score_distribution_json = Column(Text)  # ✅ 긴 문자열 JSON 저장에 적합
