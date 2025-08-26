from pydantic_settings import BaseSettings 
from pydantic import ValidationError 
import sys
from typing import List

# Settings Class - It holds all the env variables
class Settings(BaseSettings):
    # Allowed origins (your frontend URLs go here)
    origins: List[str] = [
        "http://localhost:3000",
        "*"
        "https://your-frontend.com",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

try:
    settings = Settings()
except ValidationError as err:
    # Log the Error
    sys.exit(1)