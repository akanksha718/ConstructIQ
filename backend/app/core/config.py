from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "ConstructIQ"

    DATABASE_URL: str

    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_BUCKET: str

    CLERK_SECRET_KEY: str
    CLERK_ISSUER: str
    CLERK_JWKS_URL: str

    GEMINI_API_KEY: str
    GEMINI_LLM_MODEL: str = "gemini-3.5-flash"

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000"
    ]

    NEO4J_URI: str | None = None
    NEO4J_USER: str | None = None
    NEO4J_PASSWORD: str | None = None

    REDIS_URL: str | None = None
    QUERY_CACHE_TTL_SECONDS: int = 300

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
