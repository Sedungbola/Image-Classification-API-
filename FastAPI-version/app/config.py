from pydantic import BaseSettings, AnyHttpUrl
from typing import List
import os

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://db:27017"
    ADMIN_PW_HASH: str
    PORT: int = 5025
    CORS_ORIGINS: List[str] = ["*"]
    REQUEST_TIMEOUT: int = 10
    MAX_IMAGE_SIZE_MB: int = 8
    class Config:
        env_file = ".env"

settings = Settings()