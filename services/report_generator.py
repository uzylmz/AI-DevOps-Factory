from services.devops_assessment import (
    compute_devops_score,
    get_maturity_level
)

from services.devops_options import (
    CI_CD_PLATFORM_DISPLAY_NAMES,
    CI_CD_PLATFORM_ASSET_KEYS,
    DELIVERY_METHOD_DISPLAY_NAMES
)


def generate_devops_report(
    specification,
    gap_report: dict
) -> str:

    assets = gap_report["assets"]
    gaps = gap_report["gaps"]

    platform = gap_report[
        "selected_ci_cd_platform"
    ]

    delivery_method = gap_report[
        "selected_delivery_method"
    ]

    platform_label = (
        CI_CD_PLATFORM_DISPLAY_NAMES.get(
            platform,
            platform
        )
    )

    delivery_label = (
        DELIVERY_METHOD_DISPLAY_NAMES.get(
            delivery_method,
            delivery_method
        )
    )

    pipeline_asset_key = (
        CI_CD_PLATFORM_ASSET_KEYS.get(
            platform
        )
    )

    pipeline_present = assets.get(
        pipeline_asset_key,
        False
    )

    score = compute_devops_score(
        assets,
        delivery_method,
        platform
    )

    maturity = get_maturity_level(
        score
    )

    report = f"""
==================================
DEVOPS ASSESSMENT REPORT
==================================

Project:
{specification.project_name}

Language:
{specification.language}

Framework:
{specification.framework}

Database:
{specification.database}

Build Tool:
{specification.build_tool}

CI/CD Platform:
{platform_label}

Delivery Method:
{delivery_label}

----------------------------------
DEVOPS ASSETS
----------------------------------

README:
{"Present" if assets["readme"] else "Missing"}

GitIgnore:
{"Present" if assets["gitignore"] else "Missing"}

{platform_label} Pipeline:
{"Present" if pipeline_present else "Missing"}
"""

    if delivery_method == "container_image":

        report += f"""
Dockerfile:
{"Present" if assets["dockerfile"] else "Missing"}

Docker Compose:
{"Present" if assets["docker_compose"] else "Missing"}
"""

    else:

        report += """
Containerization:
Not required for the selected delivery method.
"""

    report += f"""
----------------------------------
DEVOPS MATURITY
----------------------------------

Score:
{score}/100

Level:
{maturity}

----------------------------------
RECOMMENDATIONS
----------------------------------
"""

    recommendations = []

    if gaps["generate_pipeline"]:

        recommendations.append(
            f"Generate {platform_label} pipeline"
        )

    if gaps["generate_dockerfile"]:

        recommendations.append(
            "Generate Dockerfile"
        )

    if gaps["generate_docker_compose"]:

        recommendations.append(
            "Generate docker-compose.yml"
        )

    if gaps["generate_readme"]:

        recommendations.append(
            "Generate README"
        )

    if gaps["generate_gitignore"]:

        recommendations.append(
            "Generate .gitignore"
        )

    if not recommendations:

        recommendations.append(
            "No basic DevOps remediation is required"
        )

    for recommendation in recommendations:

        report += (
            f"\n- {recommendation}"
        )

    return report.strip()