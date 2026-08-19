import json

from models.project_spec import ProjectSpec
from services.llm_service import ask_llm


def analyze_project(prompt: str):

    llm_prompt = f"""
You are a DevOps Architect.

Analyze the user request.

Return ONLY valid JSON.

Expected format:

{{
    "project_name": "short-project-name",
    "backend": "",
    "database": "",
    "cloud": "",
    "tests": [],
    "environments": []
}}

project_name must never be empty.
Generate a meaningful kebab-case project name.

User request:

{prompt}
"""

    response = ask_llm(llm_prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    data = json.loads(response)

    return ProjectSpec(**data)