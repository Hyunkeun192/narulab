# narulab/models/report_sten_distribution.py

from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.database.database import Base
from uuid import uuid4
import enum

# ✅ 분포 집계 기준 그룹 enum
class GroupTypeEnum(str, enum.Enum):
    overall = "overall"
    school = "school"
    region = "region"
    company = "company"

# ✅ STEN 분포 저장 테이블
class ReportSTENDistribution(Base):
    __tablename__ = "report_sten_distribution"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.test_id"), nullable=False)
    group_type = Column(Enum(GroupTypeEnum), nullable=False)   # 예: school
    group_value = Column(String, nullable=True)                # 예: 서울대
    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)

    # ✅ STEN 1~10 점수대별 응답자 수
    sten_1 = Column(Integer, default=0)
    sten_2 = Column(Integer, default=0)
    sten_3 = Column(Integer, default=0)
    sten_4 = Column(Integer, default=0)
    sten_5 = Column(Integer, default=0)
    sten_6 = Column(Integer, default=0)
    sten_7 = Column(Integer, default=0)
    sten_8 = Column(Integer, default=0)
    sten_9 = Column(Integer, default=0)
    sten_10 = Column(Integer, default=0)
