from openai import OpenAI

from google import genai

from groq import Groq

from app.core.config import (
    settings
)


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

        if provider=="modelscope":

            return OpenAI(

                api_key=

                settings.MODELSCOPE_API_KEY,

                base_url=

                "https://api-inference.modelscope.cn/v1"

            )

        raise ValueError(

            f"Unsupported provider: {provider}"

        )

    @staticmethod
    def get_model():

        return (

            settings.AI_MODEL

        )