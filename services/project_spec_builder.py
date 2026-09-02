from agents.repository_analyzer_agent.agent import (
    analyze_repository_with_llm
)

from models.project_spec import ProjectSpec


def build_project_spec_from_repository(
    project_path: str
):

    analysis = analyze_repository_with_llm(
        project_path
    )

    language = analysis.get(
        "language",
        "unknown"
    ).lower()

    framework = analysis.get(
        "framework",
        "unknown"
    ).lower()

    database = analysis.get(
        "database",
        "unknown"
    ).lower()

    build_tool = analysis.get(
        "build_tool",
        "unknown"
    ).lower()

    return ProjectSpec(
        project_name=f"{language}-project",
        language=language,
        framework=framework,
        database=database,
        build_tool=build_tool,
        cloud="unknown",
        environments=["dev"],
        docker=True,
        ci_cd=True,
        kubernetes=False,
        terraform=False
    )