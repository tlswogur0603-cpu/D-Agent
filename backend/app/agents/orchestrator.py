import json
from typing import List

import google.generativeai as genai
from pydantic import ValidationError

from app.agents.tools.log_tool import get_logs_for_ai
from app.core.config import settings
from app.schemas.agent import LogAnalysisResponse


def _build_error_response(message: str) -> LogAnalysisResponse:
    # analyze_logs는 어떤 경우에도 API 레이어에서 그대로 반환 가능한
    # LogAnalysisResponse 형태를 유지하도록 실패 응답을 표준화합니다.
    return LogAnalysisResponse(
        error_summary=message,
        risk_score=1,
        detected_issues=["AI 분석 실패"],
        suggested_solutions=[
            "GEMINI_API_KEY 설정 여부를 확인하세요.",
            "네트워크 연결 상태를 확인한 뒤 다시 시도하세요.",
            "동일 증상이 지속되면 로그 샘플과 함께 운영자에게 문의하세요.",
        ],
    )


# ------------------------------------------------------------
# 모델 초기화(서버 실행 시 1회): configure + 모델 객체 생성
# ------------------------------------------------------------
# - analyze_logs 호출마다 재초기화하지 않고, 모듈 로딩 시 한 번만 준비해 재사용합니다.
# - GEMINI_API_KEY가 누락된 경우 config 단계에서 이미 실패(Strict)해야 하므로 여기서는 예외를 숨기지 않습니다.
genai.configure(api_key=settings.GEMINI_API_KEY)
_MODEL = genai.GenerativeModel("gemini-2.5-flash")


def analyze_logs(raw_logs: List[str]) -> LogAnalysisResponse:
    """
    원본 로그 문자열 목록(raw_logs)을 입력받아 보안 관점으로 분석한 뒤,
    `LogAnalysisResponse` 스키마 형태의 결과를 반환합니다.
    """
    logs_for_ai = get_logs_for_ai(raw_logs)

    # 모델이 자유 텍스트로 이탈하지 않도록 출력 스키마를 프롬프트에 명시해
    # 후속 JSON 파싱과 Pydantic 검증 성공률을 높입니다.
    logs_json = json.dumps(logs_for_ai, ensure_ascii=False)
    prompt = f"""당신은 보안 로그 분석가입니다. 아래 로그를 바탕으로 보안 관점에서 분석하세요.
모든 분석 결과는 반드시 한국어로 작성하라.
반드시 JSON 객체만 반환하고, 키는 다음 4개만 사용하세요:
error_summary(string), risk_score(int 1~10), detected_issues(string[]), suggested_solutions(string[])

로그 데이터:
{logs_json}"""

    # 응답 MIME 타입을 JSON으로 강제해 모델 출력 형식을 고정하고,
    # json.loads -> LogAnalysisResponse 검증 파이프라인을 안정화합니다.
    try:
        response = _MODEL.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )

        parsed = json.loads(response.text)
        return LogAnalysisResponse(**parsed)
    except json.JSONDecodeError:
        return _build_error_response(
            "AI 분석 결과를 처리하는 중 오류가 발생했습니다. (JSON 파싱 실패)"
        )
    except ValidationError:
        return _build_error_response(
            "AI 분석 결과 형식이 올바르지 않습니다. (응답 스키마 검증 실패)"
        )
    except Exception as e:
        return _build_error_response(
            f"AI 분석 중 예기치 못한 오류가 발생했습니다. 잠시 후 다시 시도해주세요. ({type(e).__name__})"
        )

