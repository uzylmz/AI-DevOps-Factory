import os

from dotenv import load_dotenv

from services.azure_provider import ask_azure
from services.lmstudio_provider import ask_lmstudio

load_dotenv()


def ask_llm(prompt):

    provider = os.getenv(
        "LLM_PROVIDER",
        "lmstudio"
    )

    if provider == "azure":
        return ask_azure(prompt)

    return ask_lmstudio(prompt)
