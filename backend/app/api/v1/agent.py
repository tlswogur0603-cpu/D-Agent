from fastapi import APIRouter, HTTPException

from app.agents.orchestrator import analyze_logs
from app.schemas.agent import LogAnalysisRequest, LogAnalysisResponse


router = APIRouter()


@router.post("/analyze", response_model=LogAnalysisResponse)
def analyze(request: LogAnalysisRequest) -> LogAnalysisResponse:
    if not request.logs:
        raise HTTPException(status_code=400, detail="분석할 로그 데이터가 없습니다.")

    try:
        return analyze_logs(request.logs)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "로그 분석 중 오류가 발생했습니다. "
                "API 키 설정 및 네트워크 연결 상태를 확인한 뒤 다시 시도해주세요."
            ),
        )

