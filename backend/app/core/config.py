from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    cors_allow_origins: list[str] = Field(default_factory=lambda: ["*"])
    jwt_secret_key: str = Field("change-me", env="AUDai_JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60 * 24 * 30
    s3_bucket: str = Field(..., env="AUDAI_S3_BUCKET")
    s3_region: str = Field(..., env="AUDAI_S3_REGION")
    database_url: str = Field(..., env="AUDAI_DATABASE_URL")
    redis_url: str = Field(..., env="AUDAI_REDIS_URL")
    hf_token: str | None = Field(default=None, env="HF_TOKEN")
    gpt_oss_endpoint: str = Field(..., env="GPT_OSS_ENDPOINT")
    gpt_oss_api_key: str = Field(..., env="GPT_OSS_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]


settings = get_settings()
