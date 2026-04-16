from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

import os


_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_ENV_FILE = os.path.join(_PROJECT_ROOT, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    GEMINI_API_KEY: str = "this-is-fake-key-for-now"
    PROJECT_NAME: str = "D-Agent"
    DEBUG: bool = True


settings = Settings()
