import asyncio
import hashlib
import logging
import time

from app.ai.cache_handler import (
    CacheHandler
)

from app.ai.fallback_handler import (
    FallbackHandler
)

from app.ai.llm_factory import (
    LLMFactory
)

from app.ai.prompt_guard import (
    PromptGuard
)

from app.ai.prompt_loader import (
    PromptLoader
)

from app.core.config import (
    settings
)


logger = logging.getLogger(

    __name__

)


class AIService:

    CACHE_ENABLED = True

    MAX_RETRIES = 2

    REQUEST_TIMEOUT = 30

    GROQ_TEMPERATURE = 0.15

    MAX_OUTPUT_TOKENS = 120

    def __init__(

        self

    ):

        self.client = (

            LLMFactory
            .get_client()

        )

        self.model = (

            LLMFactory
            .get_model()

        )

        self.cache = (

            CacheHandler()

        )

        self.provider = (

            settings
            .AI_PROVIDER
            .lower()

        )

    async def execute_prompt(

        self,

        prompt: str

    ):

        start = time.time()

        try:

            PromptGuard.validate(

                prompt

            )

            cache_key = (

                hashlib.md5(

                    (

                        self.provider
                        +
                        self.model
                        +
                        prompt

                    ).encode()

                )

                .hexdigest()

            )

            if self.CACHE_ENABLED:

                cached = (

                    await self.cache.get(

                        cache_key

                    )

                )

                if cached:

                    logger.info(

                        "CACHE HIT"

                    )

                    return cached

            response = None

            for attempt in range(

                self.MAX_RETRIES + 1

            ):

                try:

                    logger.info(

                        "%s ATTEMPT %s",

                        self.provider,

                        attempt + 1

                    )

                    response = await (

                        asyncio.wait_for(

                            asyncio.to_thread(

                                self._generate,

                                prompt

                            ),

                            timeout=

                            self.REQUEST_TIMEOUT

                        )

                    )

                    break

                except Exception:

                    if (

                        attempt

                        >=

                        self.MAX_RETRIES

                    ):

                        raise

                    await asyncio.sleep(

                        1

                    )

            if not response:

                raise RuntimeError(

                    "Empty AI response"

                )

            latency = round(

                (

                    time.time()

                    -

                    start

                )

                *

                1000,

                2

            )

            result = {

                "success": True,

                "response":

                response.strip(),

                "error": None,

                "metadata": {

                    "provider":

                    self.provider,

                    "model":

                    self.model,

                    "latency_ms":

                    latency

                }

            }

            if self.CACHE_ENABLED:

                await self.cache.set(

                    cache_key,

                    result

                )

            logger.info(

                "AI SUCCESS %sms",

                latency

            )

            return result

        except asyncio.TimeoutError:

            logger.exception(

                "LLM TIMEOUT"

            )

            return (

                FallbackHandler
                .get_fallback_response()

            )

        except Exception as e:

            logger.exception(

                "LLM FAILURE"

            )

            return {

                "success": False,

                "response": None,

                "error": str(

                    e

                )

            }

    def _generate(

        self,

        prompt: str

    ):

        if (

            self.provider

            ==

            "groq"

        ):

            response = (

                self.client
                .chat
                .completions
                .create(

                    model=

                    self.model,

                    messages=[

                        {

                            "role":"user",

                            "content":

                            prompt

                        }

                    ],

                    temperature=

                    self.GROQ_TEMPERATURE,

                    max_tokens=

                    self.MAX_OUTPUT_TOKENS

                )

            )

            return (

                response
                .choices[0]
                .message.content

            )

        response = (

            self.client
            .models
            .generate_content(

                model=

                self.model,

                contents=

                prompt

            )

        )

        return response.text

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

        final_prompt = (

            f"{template}\n\n"

            f"{user_input}"

        )

        return await (

            self.execute_prompt(

                final_prompt

            )

        )