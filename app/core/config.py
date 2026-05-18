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

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    # -----------------------------
    # ENV CONFIGURATION
    # -----------------------------

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings() # type: ignore