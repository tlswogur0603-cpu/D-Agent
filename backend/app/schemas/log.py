from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field


class LogRead(BaseModel):
    id: int = Field(description="로그 레코드의 고유 식별자(ID)입니다.")
    timestamp: datetime = Field(description="로그가 기록된 시각(UTC 권장)입니다.")
    level: str = Field(description="로그 레벨입니다. 예: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    service_name: str = Field(description="로그를 발생시킨 서비스/모듈 이름입니다.")
    message: str = Field(description="로그의 핵심 메시지(사람이 읽는 텍스트)입니다.")
    metadata: Dict[str, Any] = Field(
        description="추가 컨텍스트를 담는 임의의 구조화 데이터입니다. 예: request_id, user_id, payload 등"
    )

