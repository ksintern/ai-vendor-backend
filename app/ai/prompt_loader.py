from pathlib import Path


BASE_DIR = (

    Path(__file__)

    .resolve()

    .parent

)

PROMPTS_DIR = (

    BASE_DIR

    / "prompts"

)


class PromptLoader:

    _cache = {}


    @classmethod
    def load_prompt(

        cls,

        filename: str

    ) -> str:

        cached = (

            cls._cache.get(

                filename

            )

        )

        if cached:

            return cached

        filepath = (

            PROMPTS_DIR

            / filename

        )

        if not filepath.exists():

            raise FileNotFoundError(

                f"Prompt file not found: {filename}"

            )

        content = (

            filepath.read_text(

                encoding="utf-8"

            )

        )

        cls._cache[

            filename

        ] = content

        return content


    @classmethod
    def clear_cache(

        cls

    ):

        cls._cache.clear()