from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # --- Logging Config ---
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    LOG_JSON: bool = False
    LOG_FILE: str = "logs/cinemix.log"

    class Config:
        env_file = ".env"


settings = Settings()
