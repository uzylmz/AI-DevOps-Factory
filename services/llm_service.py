import os

from dotenv import load_dotenv

from services.lmstudio_provider import (
    ask_lmstudio
)

from services.openrouter_provider import (
    ask_openrouter
)

load_dotenv()


def ask_llm(prompt):

    provider = os.getenv(
        "LLM_PROVIDER",
        "lmstudio"
    )

    if provider == "openrouter":
        return ask_openrouter(prompt)

    return ask_lmstudio(prompt)