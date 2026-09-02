import json

from models.project_spec import ProjectSpec
from services.llm_service import ask_llm


def analyze_project(prompt: str):

    llm_prompt = f"""
You are a DevOps Architect.

Analyze the user request.

Return ONLY valid JSON.
Do not add explanations.

Expected format:

{{
    "project_name": "short-project-name",
    "backend": "",
    "database": "",
    "cloud": "",
    "environments": [],
    "docker": true,
    "ci_cd": true
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

    data["backend"] = data["backend"].lower()
    data["database"] = data["database"].lower()
    data["cloud"] = data["cloud"].lower()

    if not data["project_name"]:
        data["project_name"] = f"{data['backend']}-app"


    return ProjectSpec(**data)