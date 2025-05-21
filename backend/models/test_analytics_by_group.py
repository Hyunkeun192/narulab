from sqlalchemy import Column, String, Float, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.test_id"), nullable=False)

    group_type = Column(Enum(GroupTypeEnum), nullable=False)  # ex: school, region
    group_value = Column(String, nullable=False)  # ex: 서울대, 경기지역, 삼성전자

    year = Column(Integer, nullable=True)   # ✅ 연도 기준 필터용
    month = Column(Integer, nullable=True)  # ✅ 월 기준 필터용


    avg_total_score = Column(Float, nullable=True)
    std_total_score = Column(Float, nullable=True)
    completion_rate = Column(Float, nullable=True)
    overall_correct_rate = Column(Float, nullable=True)

    score_distribution_json = Column(String, nullable=True)  # JSON 문자열로 저장 (ex: {"STEN 6": 23, "STEN 7": 45, ...})
