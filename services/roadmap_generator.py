from services.devops_options import (
    CI_CD_PLATFORM_DISPLAY_NAMES
)


def generate_devops_roadmap(
    gap_report: dict
) -> list:
    gaps = gap_report["gaps"]

    platform = gap_report[
        "selected_ci_cd_platform"
    ]

    platform_label = (
        CI_CD_PLATFORM_DISPLAY_NAMES.get(
            platform,
            platform
        )
    )

    roadmap = []
    priority = 1

    if gaps["generate_pipeline"]:

        roadmap.append({
            "priority": priority,
            "task": (
                f"Generate {platform_label} "
                "pipeline"
            ),
            "impact": (
                "Automated build and delivery"
            )
        })

        priority += 1

    if gaps["generate_dockerfile"]:

        roadmap.append({
            "priority": priority,
            "task": "Generate Dockerfile",
            "impact": (
                "Container image delivery"
            )
        })

        priority += 1

    if gaps["generate_docker_compose"]:

        roadmap.append({
            "priority": priority,
            "task": (
                "Generate docker-compose.yml"
            ),
            "impact": (
                "Local container orchestration"
            )
        })

        priority += 1

    if gaps["generate_readme"]:

        roadmap.append({
            "priority": priority,
            "task": "Generate README",
            "impact": "Project documentation"
        })

        priority += 1

    if gaps["generate_gitignore"]:

        roadmap.append({
            "priority": priority,
            "task": "Generate .gitignore",
            "impact": (
                "Source-control hygiene"
            )
        })

    return roadmap