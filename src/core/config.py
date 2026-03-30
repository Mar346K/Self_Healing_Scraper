from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"  # Fallback for local dev
    gemini_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
