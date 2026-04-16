from typing import List

from backend.app.services.log_service import get_filtered_logs


def get_logs_for_ai(logs: List[str]) -> List[List[str]]:
    """
    원본 로그 리스트에서 ERROR와 그 맥락을 추출하는 도구임

    ERROR가 발견되었을 때 AI 에이전트가 가장 먼저 호출해야 함

    내부적으로 log_service.py를 실행하여 10분 이내의 최신 에러 세트를 최대 20개 반환함
    """

    return get_filtered_logs(logs)