import os


def generate_project_structure(spec, gap_report, target_path):

    output_dir = target_path

    os.makedirs(output_dir, exist_ok=True)

    os.makedirs(
        os.path.join(output_dir, "src"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(output_dir, "docs"),
        exist_ok=True
    )

    # Dockerfile
    dockerfile_content = get_dockerfile_content(
        spec.language
    )

    if gap_report["gaps"]["generate_dockerfile"]:
        with open(
            os.path.join(output_dir, "Dockerfile"),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(dockerfile_content)

    # docker-compose
    if gap_report["gaps"]["generate_docker_compose"]:
        generate_docker_compose(
            output_dir,
            spec
        )

    # README
    readme_content = f"""
# {spec.project_name}

## Project Information

Language: {spec.language}

Framework: {spec.framework}

Database: {spec.database}

Build Tool: {spec.build_tool}

Cloud: {spec.cloud}

Environments:
{", ".join(spec.environments)}

Docker:
{spec.docker}

CI/CD:
{spec.ci_cd}

Kubernetes:
{spec.kubernetes}

Terraform:
{spec.terraform}
"""

    if gap_report["gaps"]["generate_readme"]:
        with open(
            os.path.join(output_dir, "README.md"),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(readme_content)

    # .gitignore
    if gap_report["gaps"]["generate_gitignore"]:
        generate_gitignore(output_dir)

    # Pipeline
    if spec.ci_cd:
        generate_pipeline(
            output_dir,
            gap_report
        )

    return output_dir


def get_dockerfile_content(language):

    if language == "python":
        return """
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
"""

    elif language == "java":
        return """
FROM eclipse-temurin:21-jdk

WORKDIR /app

COPY . .

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
"""

    elif language == "nodejs":
        return """
FROM node:20

WORKDIR /app

COPY . .

RUN npm install

CMD ["npm", "start"]
"""

    return """
FROM alpine:latest
"""


def generate_docker_compose(
    project_dir,
    spec
):

    content = """
services:
  app:
    build: .
    ports:
      - "8080:8080"
"""

    with open(
        os.path.join(
            project_dir,
            "docker-compose.yml"
        ),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)


def generate_gitignore(project_dir):

    content = """
.venv/
__pycache__/
.vscode/
.idea/
.env
*.log
"""

    with open(
        os.path.join(
            project_dir,
            ".gitignore"
        ),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)


def generate_pipeline(
    project_dir,
    gap_report
):

    pipeline_dir = os.path.join(
        project_dir,
        "pipelines"
    )

    os.makedirs(
        pipeline_dir,
        exist_ok=True
    )

    content = """
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:
- script: echo Building application
  displayName: Build

- script: echo Running tests
  displayName: Test
"""

    if gap_report["gaps"]["generate_pipeline"]:
        with open(
            os.path.join(
                pipeline_dir,
                "azure-pipelines.yml"
            ),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(content)