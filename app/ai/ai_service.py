import asyncio
import time

from app.ai.llm_factory import (
    LLMFactory
)

from app.ai.prompt_loader import (
    PromptLoader
)

from app.ai.fallback_handler import (
    FallbackHandler
)

from app.ai.cache_handler import (
    CacheHandler
)


class AIService:

    def __init__(self):

        self.client = LLMFactory.get_client()

        self.model = LLMFactory.get_model()

        self.cache = CacheHandler()


    async def execute_prompt(

        self,

        prompt: str

    ):

        cache_key = f"prompt:{prompt}"

        cached = await self.cache.get(

            cache_key

        )

        if cached:

            return cached

        start_time = time.time()

        try:

            response = await asyncio.to_thread(

                lambda:

                self.client.models.generate_content(

                    model=self.model,

                    contents=prompt

                )

            )

            latency = round(

                (time.time() - start_time) * 1000,

                2

            )

            result = {

                "success": True,

                "response": response.text,

                "error": None,

                "metadata": {

                    "provider": "gemini",

                    "model": self.model,

                    "latency_ms": latency,

                    "fallback": False

                }

            }

            await self.cache.set(

                cache_key,

                result

            )

            return result

        except TimeoutError:

            return (

                FallbackHandler

                .get_fallback_response()

            )

        except Exception as e:

            latency = round(

                (time.time() - start_time) * 1000,

                2

            )

            return {

                "success": False,

                "response": None,

                "error": str(e),

                "metadata": {

                    "provider": "gemini",

                    "model": self.model,

                    "latency_ms": latency,

                    "fallback": False

                }

            }


    async def execute_prompt_file(

        self,

        prompt_file: str,

        user_input: str

    ):

        template = (

            PromptLoader

            .load_prompt(

                prompt_file

            )

        )

        final_prompt = f"""

{template}

User Input:

{user_input}

"""

        return await self.execute_prompt(

            final_prompt

        )