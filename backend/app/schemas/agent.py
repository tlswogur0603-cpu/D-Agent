from typing import List

from pydantic import BaseModel, Field


class LogAnalysisRequest(BaseModel):
    logs: List[str]
    project_name: str = "default_project"


class LogAnalysisResponse(BaseModel):
    error_summary: str = Field(
        description="로그 분석 결과를 요약한 내용입니다. (예: 핵심 에러 메시지, 발생 원인 추정, 영향 범위 요약 등)"
    )
    risk_score: int = Field(
        ge=1,
        le=10,
        description=(
            "위험도 점수입니다. 1부터 10까지 int로 판단할꺼야\n"
            "description\n"
            "1~3은 Low (단순 경고) → 예시 → 단순 오타, 권한 없는 페이지 접근 등 시스템 운영에는 지장이 없는 로그.\n"
            "4~6은 Medium (불편 사항) 예시 → 특정 기능(예: 이미지 업로드)이 간헐적으로 실패함. 유저가 불편을 느끼지만 서비스 전체는 돌아감.\n"
            "7~8은 High (부분 장애) 예시 → 결제 실패, 로그인 불가능 등 주요 기능이 마비됨. 즉시 담당자에게 알림을 보내야 하는 수준.\n"
            "9~10은 Critical (전체 마비) 예시 → DB 연결 끊김, 서버 다운 등 서비스 전체가 중단됨. 5분 내 대응이 필요한 긴급 상황."
        ),
    )
    detected_issues: List[str] = Field(
        description="로그에서 감지된 문제(이슈) 목록입니다. 각 항목은 사람이 읽을 수 있는 간단한 문장/키워드로 작성합니다."
    )
    suggested_solutions: List[str] = Field(
        description="감지된 이슈를 해결하거나 완화하기 위한 제안(솔루션) 목록입니다. 각 항목은 실행 가능한 조치 형태로 작성합니다."
    )
