from pydantic_settings import (

    BaseSettings,

    SettingsConfigDict

)


class Settings(

    BaseSettings

):

    # -----------------------------
    # DATABASE
    # -----------------------------

    DATABASE_URL:str


    # -----------------------------
    # JWT
    # -----------------------------

    SECRET_KEY:str

    ALGORITHM:str="HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES:int=15

    REFRESH_TOKEN_EXPIRE_DAYS:int=7


    # -----------------------------
    # GEMINI
    # -----------------------------

    GEMINI_API_KEY:str|None=None


    # -----------------------------
    # GROQ
    # -----------------------------

    GROQ_API_KEY:str|None=None


    # -----------------------------
    # MODELSCOPE
    # -----------------------------

    MODELSCOPE_API_KEY:str|None=None


    # -----------------------------
    # AI
    # -----------------------------

    AI_PROVIDER:str="groq"

    AI_MODEL:str="llama-3.1-8b-instant"

    AI_TIMEOUT:int=45


    # -----------------------------
    # ENV
    # -----------------------------

    model_config=(

        SettingsConfigDict(

            env_file=".env",

            extra="ignore"

        )

    )


settings=Settings()  # type: ignore


print(

    "GROQ KEY:",

    settings.GROQ_API_KEY

)

print(

    "MODELSCOPE KEY:",

    settings.MODELSCOPE_API_KEY

)

print(

    "AI PROVIDER:",

    settings.AI_PROVIDER

)

print(

    "AI MODEL:",

    settings.AI_MODEL

)