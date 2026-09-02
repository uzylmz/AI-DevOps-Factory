from models.project_spec import ProjectSpec


def build_project_spec_from_repository(analysis):

    language = analysis.get(
        "language",
        "unknown"
    ).lower()

    return ProjectSpec(
        project_name=f"{language}-project",
        language=language,
        framework=analysis.get(
            "framework",
            "unknown"
        ).lower(),
        database=analysis.get(
            "database",
            "unknown"
        ).lower(),
        build_tool=analysis.get(
            "build_tool",
            "unknown"
        ).lower(),
        cloud="unknown",
        environments=["dev"],
        docker=True,
        ci_cd=True,
        kubernetes=False,
        terraform=False
    )