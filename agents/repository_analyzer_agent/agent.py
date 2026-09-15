import os
import json

from services.llm_service import ask_llm

def analyze_repository(project_path: str):

    result = {
        "language": "unknown",
        "build_tool": "unknown"
    }

    files = os.listdir(project_path)

    if "pom.xml" in files:
        result["language"] = "java"
        result["build_tool"] = "maven"

    elif "package.json" in files:
        result["language"] = "nodejs"
        result["build_tool"] = "npm"

    elif "requirements.txt" in files:
        result["language"] = "python"
        result["build_tool"] = "pip"

    return result

def read_file_content(file_path):

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    except Exception:
        return ""


def build_repository_context(project_path):

    context = ""

    files_to_analyze = [
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "Dockerfile",
    "docker-compose.yml",
    "pom.xml",
    "application.properties",
    "application.yml",
    "package.json"
    ]

    for file_name in files_to_analyze:

        file_path = os.path.join(
            project_path,
            file_name
        )

        if os.path.exists(file_path):

            context += f"\n\nFILE: {file_name}\n"

            context += read_file_content(
                file_path
            )[:5000]

    return context

import json


def analyze_stack_with_llm(context: str):

    prompt = f"""
You are a software repository and DevOps analyst.

Analyze the repository content and identify:

- language
- framework
- database
- build_tool

Return ONLY one valid JSON object.

Required format:

{{
    "language": "unknown",
    "framework": "unknown",
    "database": "unknown",
    "build_tool": "unknown"
}}

Rules:

- Never return an empty response.
- Never return empty string values.
- Use "unknown" when information cannot be detected.
- Do not add Markdown.
- Do not add code fences.
- Do not add explanations.
- Do not add text before or after the JSON.

Repository content:

{context}
"""

    response = ask_llm(prompt)

    if response is None:
        raise RuntimeError(
            "Le LLM n'a retourné aucune réponse."
        )

    response = response.strip()

    if not response:
        raise RuntimeError(
            "Le LLM a retourné une réponse vide."
        )

    print("\n=== RAW LLM RESPONSE ===")
    print(response)
    print("========================\n")

    response = response.replace("```json", "")
    response = response.replace("```JSON", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        data = json.loads(response)

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "La réponse du LLM n'est pas un JSON valide.\n"
            f"Réponse reçue :\n{response}\n\n"
            f"Erreur JSON : {error}"
        ) from error

    required_fields = [
        "language",
        "framework",
        "database",
        "build_tool"
    ]

    for field in required_fields:
        value = data.get(field)

        if value is None or str(value).strip() == "":
            data[field] = "unknown"

        elif isinstance(value, str):
            data[field] = value.strip().lower()

    return data

def analyze_repository_with_llm(
        project_path
):

    context = build_repository_context(
        project_path
    )

    return analyze_stack_with_llm(
        context
    )