from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    # -----------------------------
    # DATABASE CONFIGURATION
    # -----------------------------

    DATABASE_URL: str

    # -----------------------------
    # JWT CONFIGURATION
    # -----------------------------

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # -----------------------------
    # GEMINI CONFIGURATION
    # -----------------------------

    GEMINI_API_KEY: str | None = None

    # -----------------------------
    # AI CONFIGURATION
    # -----------------------------

    AI_PROVIDER: str = "gemini"

    AI_MODEL: str = "gemini-2.5-flash"

    AI_TIMEOUT: int = 30

    # -----------------------------
    # ENV CONFIGURATION
    # -----------------------------

    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore"

    )


settings = Settings()  # type: ignore