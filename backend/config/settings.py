from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    max_file_size: int = 10485760
    cors_origins: list[str] = ["*"] if env == "development" else []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 