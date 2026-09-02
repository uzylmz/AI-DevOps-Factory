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
        "pom.xml",
        "package.json",
        "requirements.txt",
        "README.md"
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

def analyze_stack_with_llm(context):

    prompt = f"""
Analyze this software project.

Return ONLY valid JSON.

{{
    "language": "",
    "framework": "",
    "database": "",
    "build_tool": ""
}}

Repository content:

{context}
"""

    response = ask_llm(prompt)

    response = response.replace(
        "```json",
        ""
    )

    response = response.replace(
        "```",
        ""
    )

    response = response.strip()

    return json.loads(response)

def analyze_repository_with_llm(
        project_path
):

    context = build_repository_context(
        project_path
    )

    return analyze_stack_with_llm(
        context
    )