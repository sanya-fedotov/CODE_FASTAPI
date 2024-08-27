from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "ERROR", "CRITICAL"]
    model_config = SettingsConfigDict(env_file=".env")
    
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = None

    @model_validator(mode="before")
    def get_database_url(cls, v):
        v["DATABASE_URL"] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return v
    
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str
    TEST_DATABASE_URL: str = None

    @model_validator(mode="before")
    def get_test_database_url(cls, v):
        v["TEST_DATABASE_URL"] = f"postgresql+asyncpg://{v['TEST_DB_USER']}:{v['TEST_DB_PASS']}@{v['TEST_DB_HOST']}:{v['TEST_DB_PORT']}/{v['TEST_DB_NAME']}"
        return v
    
    SECRET_KEY: str
    ALGORITHM: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    
    REDIS_HOST: str
    REDIS_PORT: int

settings = Settings()

print(settings.DATABASE_URL)
