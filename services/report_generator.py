from services.devops_assessment import (
    compute_devops_score,
    get_maturity_level
)


def generate_devops_report(
    specification,
    assets,
    gaps
):

    score = compute_devops_score(
        assets
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

----------------------------------
DEVOPS ASSETS
----------------------------------

Dockerfile:
{"Present" if assets["dockerfile"] else "Missing"}

Docker Compose:
{"Present" if assets["docker_compose"] else "Missing"}

Azure Pipeline:
{"Present" if assets["azure_pipeline"] else "Missing"}

GitIgnore:
{"Present" if assets["gitignore"] else "Missing"}

GitHub Actions:
{"Present" if assets["github_actions"] else "Missing"}

Kubernetes:
{"Present" if assets["kubernetes"] else "Missing"}

Terraform:
{"Present" if assets["terraform"] else "Missing"}

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

    if gaps["generate_dockerfile"]:
        report += "\n- Generate Dockerfile"

    if gaps["generate_docker_compose"]:
        report += "\n- Generate docker-compose.yml"

    if gaps["generate_pipeline"]:
        report += "\n- Generate Azure Pipeline"

    if gaps["generate_readme"]:
        report += "\n- Generate README"

    if not assets["kubernetes"]:
        report += "\n- Evaluate Kubernetes deployment"

    if not assets["terraform"]:
        report += "\n- Evaluate Infrastructure as Code with Terraform"

    if not assets["github_actions"]:
        report += "\n- Add GitHub Actions workflow"

    return report