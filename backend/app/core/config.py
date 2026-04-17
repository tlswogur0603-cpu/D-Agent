import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

"""
[중앙 설정 관리 모듈]
프로젝트 전체에서 사용하는 환경 변수(API 키, 서버 설정 등)를 한곳에서 관리합니다.
.env 파일을 서버 시작 시 로드하고, 필수 환경 변수는 누락 시 즉시 에러가 나도록(Strict) 설정합니다.
"""

# 경로 설정: 프로젝트 어느 위치에서 실행해도 .env 파일을 찾을 수 있도록 절대 경로를 계산합니다.
# __file__(현재 파일 위치) 기준 상위로 2번 이동하여 루트 디렉토리(D-Agent/)를 찾습니다.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_ENV_FILE = os.path.join(_PROJECT_ROOT, ".env")

# ------------------------------------------------------------
# python-dotenv 로드: 서버 시작 시 .env 파일을 OS 환경 변수로 반영
# ------------------------------------------------------------
# - Pydantic Settings도 env_file을 읽을 수 있지만,
#   실무에서는 python-dotenv로 먼저 로드해두면 다른 라이브러리/코드에서도
#   동일한 환경 변수 값을 일관되게 참조할 수 있어 운영이 편합니다.
# - override=False로 두어, 이미 설정된 OS 환경 변수가 있다면 그 값을 우선합니다.
load_dotenv(dotenv_path=_ENV_FILE, override=False)


class Settings(BaseSettings):
    """
    Pydantic Settings를 사용한 환경 변수 검증 및 로드 클래스
    """
    # Pydantic 설정: .env 파일의 위치와 인코딩을 지정합니다.
    # extra="ignore"는 클래스에 정의되지 않은 변수가 .env에 있어도 에러를 내지 말라는 뜻입니다.
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 환경 변수 정의
    # .env 또는 OS 환경 변수에 값이 반드시 있어야 합니다.
    # (기본값을 두지 않으면 Settings() 생성 시점에 누락을 검증하고 서버가 즉시 실패합니다.)
    GEMINI_API_KEY: str
    PROJECT_NAME: str = "D-Agent"
    DEBUG: bool = True

# 싱글톤 패턴: 다른 파일에서 이 'settings' 객체를 임포트하여 설정값에 접근합니다.
# 예: from app.core.config import settings -> settings.GEMINI_API_KEY
settings = Settings()
