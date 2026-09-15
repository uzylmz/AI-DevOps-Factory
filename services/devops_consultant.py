from services.llm_service import ask_llm


def generate_executive_summary(
    specification,
    gap_report
):

    prompt = f"""
You are a Senior DevOps Consultant.

Analyze the following project.

PROJECT SPECIFICATION

Project Name:
{specification.project_name}

Language:
{specification.language}

Framework:
{specification.framework}

Database:
{specification.database}

Build Tool:
{specification.build_tool}

Cloud:
{specification.cloud}

DEVOPS ASSETS

Dockerfile:
{gap_report["assets"]["dockerfile"]}

Docker Compose:
{gap_report["assets"]["docker_compose"]}

Azure Pipeline:
{gap_report["assets"]["azure_pipeline"]}

GitIgnore:
{gap_report["assets"]["gitignore"]}

GitHub Actions:
{gap_report["assets"]["github_actions"]}

Kubernetes:
{gap_report["assets"]["kubernetes"]}

Terraform:
{gap_report["assets"]["terraform"]}

DEVOPS GAPS

{gap_report["gaps"]}

Write a professional DevOps assessment.

Structure:

1. Executive Summary

2. Current DevOps Maturity

3. Key Risks

4. Recommendations

5. Improvement Roadmap

Use clear and professional language.

Do not return JSON.
"""

    return ask_llm(prompt)