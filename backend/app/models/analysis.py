"""
분석 히스토리를 DB에 저장하는 `analysis_logs` ORM 모델입니다.
PK는 UUID(uuid4)로 충돌 위험을 낮추고, 구조화 결과(리스트/객체)는 PostgreSQL JSONB로 그대로 저장합니다.
모델은 `Base`를 상속해 SQLAlchemy가 테이블 매핑 대상으로 인식하도록 합니다.
"""

import uuid

from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.core.database import Base


class AnalysisLog(Base):
    __tablename__ = "analysis_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    raw_log = Column(JSONB, nullable=False)
    error_summary = Column(Text)
    risk_score = Column(Integer)
    detected_issues = Column(JSONB)
    suggested_solutions = Column(JSONB)

