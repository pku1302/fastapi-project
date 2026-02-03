import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

env_file = ".env.test" if os.getenv("ENV") == "test" else ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=env_file)
    
@lru_cache
def get_settings():
    return Settings()