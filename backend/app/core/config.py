from pydantic_settings import BaseSettings, SettingsConfigDict

import os

"""
[중앙 설정 관리 모듈]
프로젝트 전체에서 사용하는 환경 변수(API 키, 서버 설정 등)를 한곳에서 관리합니다.
.env 파일의 값을 우선적으로 읽으며, 값이 없을 경우 기본값을 사용합니다.
"""

# 경로 설정: 프로젝트 어느 위치에서 실행해도 .env 파일을 찾을 수 있도록 절대 경로를 계산합니다.
# __file__(현재 파일 위치) 기준 상위로 3번 이동하여 루트 디렉토리(D-Agent/)를 찾습니다.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_ENV_FILE = os.path.join(_PROJECT_ROOT, ".env")


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
    # .env에 값이 있으면 그 값을 쓰고, 없으면 우측의 기본값을 사용합니다.
    # 학원 공용 환경 보안을 위해 실제 키 대신 가짜 키를 기본값으로 설정했습니다.
    GEMINI_API_KEY: str = "this-is-fake-key-for-now"
    PROJECT_NAME: str = "D-Agent"
    DEBUG: bool = True

# 싱글톤 패턴: 다른 파일에서 이 'settings' 객체를 임포트하여 설정값에 접근합니다.
# 예: from app.core.config import settings -> settings.GEMINI_API_KEY
settings = Settings()
