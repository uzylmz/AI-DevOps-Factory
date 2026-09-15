import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    base_url="https://openrouter.ai/api/v1"
)


def ask_openrouter(prompt):

    response = client.chat.completions.create(
        model=os.getenv(
            "OPENROUTER_MODEL"
        ),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content