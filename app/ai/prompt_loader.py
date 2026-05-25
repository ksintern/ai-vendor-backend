from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

PROMPTS_DIR = BASE_DIR / "prompts"


class PromptLoader:


    @staticmethod
    def load_prompt(

        filename: str

    ) -> str:

        filepath = PROMPTS_DIR / filename

        if not filepath.exists():

            raise FileNotFoundError(

                f"Prompt file not found: {filename}"

            )

        return filepath.read_text(

            encoding="utf-8"

        )