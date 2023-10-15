from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path("../.env"), env_file_encoding='utf-8')

    database_hostname: str
    database_port: str
    redis_hostname: str
    redis_port: str
    database_password: str
    database_name: str
    database_username: str
    access_token_expire: int
    refresh_token_expire: int
    jwt_secret: str
    jwt_algorithm: str


settings = Settings()
