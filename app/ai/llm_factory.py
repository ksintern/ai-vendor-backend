from google import genai

from groq import Groq

from app.core.config import settings


class LLMFactory:


    @staticmethod
    def get_client():

        provider=(

            settings

            .AI_PROVIDER

            .lower()

        )

        if provider=="gemini":

            return genai.Client(

                api_key=

                settings.GEMINI_API_KEY

            )

        if provider=="groq":

            return Groq(

                api_key=

                settings.GROQ_API_KEY

            )

        raise ValueError(

            f"Unsupported provider: {provider}"

        )


    @staticmethod
    def get_model():

        return (

            settings.AI_MODEL

        )