# backend/models/report_sten_distribution.py

from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from backend.database.database import Base
from uuid import uuid4
import enum

# ✅ 분포 집계 기준 그룹 enum
class GroupTypeEnum(str, enum.Enum):
    overall = "overall"     # 전체 사용자 기준
    school = "school"       # 학교 기준
    region = "region"       # 지역 기준
    company = "company"     # 회사 기준

# ✅ STEN 분포 저장 테이블
class ReportSTENDistribution(Base):
    __tablename__ = "report_sten_distribution"

    # ✅ UUID → String(36)으로 변경 (MySQL 호환을 위해)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # UUID 문자열 기본키

    # ✅ UUID → String(36), ForeignKey 유지
    test_id = Column(String(36), ForeignKey("tests.test_id"), nullable=False)  # 검사 ID

    group_type = Column(Enum(GroupTypeEnum), nullable=False)  # 예: school, region 등

    # ✅ VARCHAR 길이 명시 (MySQL은 필수)
    group_value = Column(String(100), nullable=True)  # 예: 서울대, 강남구 등

    year = Column(Integer, nullable=True)   # 연도 필터링
    month = Column(Integer, nullable=True)  # 월 필터링

    # ✅ STEN 1~10 점수대별 응답자 수
    sten_1 = Column(Integer, default=0)   # STEN 1점 응답자 수
    sten_2 = Column(Integer, default=0)
    sten_3 = Column(Integer, default=0)
    sten_4 = Column(Integer, default=0)
    sten_5 = Column(Integer, default=0)
    sten_6 = Column(Integer, default=0)
    sten_7 = Column(Integer, default=0)
    sten_8 = Column(Integer, default=0)
    sten_9 = Column(Integer, default=0)
    sten_10 = Column(Integer, default=0)
