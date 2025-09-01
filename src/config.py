from pydantic_settings import BaseSettings
from pydantic import ValidationError, AnyUrl, Field, model_validator
from typing import List, Literal
from src.utils import logger
import sys


# Settings Class - It holds all the env variables
class Settings(BaseSettings):
    # Redis Variables
    REDIS_URL: AnyUrl
    REDIS_PASSWORD: str = Field(..., min_length=1)
    REDIS_DB: int = Field(..., ge=0)
    CACHE_TTL: int = 3600

    # Rate Limiter Variables
    BUCKET_SIZE: int = Field(..., ge=1)
    WINDOW_SIZE: int = Field(..., ge=1)
    MAX_THRESHOLD: int = Field(..., ge=1, le=1000)

    # Rate Limiter Custom Validation
    @model_validator(mode="after")
    def rate_limiter_custom_validations(self):
        if self.BUCKET_SIZE % 5 != 0 or self.WINDOW_SIZE % 5 != 0:
            raise ValueError("BUCKET_SIZE and WINDOW_SIZE must be a multiple of 5")
        if self.BUCKET_SIZE > self.WINDOW_SIZE / 2:
            raise ValueError("BUCKET_SIZE cannot exceed half of WINDOW_SIZE")
        return self

    # Allowed origins (frontend URLs go here)
    origins: List[str] = [
        "http://localhost:3000",
        "*https://your-frontend.com",
    ]

    # LOG Level Variables
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    LOG_JSON: bool = False
    LOG_FILE: str = "logs/cinemix.log"

    # Load from local .env
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()  # type:ignore
except ValidationError as err:
    logger.error(f"Error while parsing enviornment variables: {err}")
    sys.exit(1)
