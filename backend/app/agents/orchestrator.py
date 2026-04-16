import json
from typing import List

import google.generativeai as genai

from app.agents.tools.log_tool import get_logs_for_ai
from app.core.config import settings
from app.schemas.agent import LogAnalysisResponse


def analyze_logs(raw_logs: List[str]) -> LogAnalysisResponse:
    """
    원본 로그 문자열 목록(raw_logs)을 입력받아 보안 관점으로 분석한 뒤,
    `LogAnalysisResponse` 스키마 형태의 결과를 반환합니다.
    """
    # 개발 초기/로컬 환경에서 키 미설정으로 서버 전체가 실패하지 않도록
    # 가짜 키를 감지하면 즉시 안전한 안내 응답을 반환합니다.
    if settings.GEMINI_API_KEY == "this-is-fake-key-for-now":
        return LogAnalysisResponse(
            error_summary="로그 분석 중 키 오류 발생: API 키를 설정해주세요.",
            risk_score=1,
            detected_issues=["API 키 미설정"],
            suggested_solutions=[".env 파일에 GEMINI_API_KEY를 설정하세요."],
        )

    logs_for_ai = get_logs_for_ai(raw_logs)

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # 모델이 자유 텍스트로 이탈하지 않도록 출력 스키마를 프롬프트에 명시해
    # 후속 JSON 파싱과 Pydantic 검증 성공률을 높입니다.
    prompt = (
        "당신은 보안 로그 분석가입니다. 아래 로그를 바탕으로 보안 관점에서 분석하세요.\n"
        "반드시 JSON 객체만 반환하고, 키는 다음 4개만 사용하세요:\n"
        "error_summary(string), risk_score(int 1~10), detected_issues(string[]), suggested_solutions(string[])\n\n"
        f"로그 데이터:\n{json.dumps(logs_for_ai, ensure_ascii=False)}"
    )

    # 응답 MIME 타입을 JSON으로 강제해 모델 출력 형식을 고정하고,
    # json.loads -> LogAnalysisResponse 검증 파이프라인을 안정화합니다.
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"},
    )

    parsed = json.loads(response.text)
    return LogAnalysisResponse(**parsed)

