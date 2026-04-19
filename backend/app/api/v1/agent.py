import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.agents.orchestrator import analyze_logs
from app.core.database import get_db
from app.models.analysis import AnalysisLog
from app.schemas.agent import LogAnalysisRequest, LogAnalysisResponse


router = APIRouter()
_LOGGER = logging.getLogger(__name__)


@router.post("/analyze", response_model=LogAnalysisResponse)
def analyze(
    request: LogAnalysisRequest,
    db: Session = Depends(get_db),
) -> LogAnalysisResponse:
    if not request.logs:
        raise HTTPException(status_code=400, detail="분석할 로그 데이터가 없습니다.")

    try:
        result = analyze_logs(request.logs)

        try:
            row = AnalysisLog(
                raw_log=request.logs,
                error_summary=result.error_summary,
                risk_score=result.risk_score,
                detected_issues=result.detected_issues,
                suggested_solutions=result.suggested_solutions,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
        except Exception:
            _LOGGER.exception("분석 결과 DB 저장에 실패했습니다.")
            db.rollback()

        return result
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "로그 분석 중 오류가 발생했습니다. "
                "API 키 설정 및 네트워크 연결 상태를 확인한 뒤 다시 시도해주세요."
            ),
        )

