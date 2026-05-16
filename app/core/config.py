from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Database
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/your_database"
    )

    # JWT Configuration
    SECRET_KEY: str = (
        "your_super_secure_secret_key"
    )

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()