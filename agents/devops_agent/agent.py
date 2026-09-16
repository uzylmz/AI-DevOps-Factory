import os


def generate_project_structure(
    spec,
    gap_report,
    target_path
):

    output_dir = target_path

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    gaps = gap_report["gaps"]

    if gaps["generate_dockerfile"]:

        dockerfile_content = (
            get_dockerfile_content(
                spec.language
            )
        )

        write_file(
            os.path.join(
                output_dir,
                "Dockerfile"
            ),
            dockerfile_content
        )

    if gaps["generate_docker_compose"]:

        generate_docker_compose(
            output_dir,
            spec
        )

    if gaps["generate_readme"]:

        generate_readme(
            output_dir,
            spec,
            gap_report
        )

    if gaps["generate_gitignore"]:

        generate_gitignore(
            output_dir,
            spec.language
        )

    if (
        spec.ci_cd
        and gaps["generate_pipeline"]
    ):

        generate_pipeline(
            output_dir,
            gap_report,
            spec
        )

    return output_dir


def write_file(
    file_path: str,
    content: str
):

    parent_directory = os.path.dirname(
        file_path
    )

    if parent_directory:

        os.makedirs(
            parent_directory,
            exist_ok=True
        )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            content.strip() + "\n"
        )


def get_dockerfile_content(
    language: str
) -> str:

    normalized_language = (
        language.lower().strip()
    )

    if normalized_language == "python":

        return """
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
"""

    if normalized_language == "java":

        return """
FROM eclipse-temurin:21-jre

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
"""

    if normalized_language in {
        "node",
        "nodejs",
        "javascript",
        "typescript"
    }:

        return """
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
"""

    return """
FROM alpine:latest

WORKDIR /app

COPY . .

CMD ["sh"]
"""


def generate_docker_compose(
    project_dir: str,
    spec
):

    language = spec.language.lower()

    if language == "python":
        port = "8000:8000"

    elif language == "java":
        port = "8080:8080"

    else:
        port = "3000:3000"

    content = f"""
services:
  app:
    build:
      context: .
    ports:
      - "{port}"
    restart: unless-stopped
"""

    write_file(
        os.path.join(
            project_dir,
            "docker-compose.yml"
        ),
        content
    )


def generate_readme(
    project_dir: str,
    spec,
    gap_report: dict
):

    platform = gap_report[
        "selected_ci_cd_platform"
    ]

    delivery_method = gap_report[
        "selected_delivery_method"
    ]

    content = f"""
# {spec.project_name}

## Project Information

Language: {spec.language}

Framework: {spec.framework}

Database: {spec.database}

Build Tool: {spec.build_tool}

Cloud: {spec.cloud}

Environments:
{", ".join(spec.environments)}

CI/CD Platform:
{platform}

Delivery Method:
{delivery_method}
"""

    write_file(
        os.path.join(
            project_dir,
            "README.md"
        ),
        content
    )


def generate_gitignore(
    project_dir: str,
    language: str
):

    common_content = """
.env
*.log
.vscode/
.idea/
.DS_Store
Thumbs.db
"""

    language = language.lower()

    if language == "python":

        specific_content = """
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
dist/
build/
*.egg-info/
"""

    elif language == "java":

        specific_content = """
target/
*.class
*.jar
.gradle/
build/
"""

    elif language in {
        "node",
        "nodejs",
        "javascript",
        "typescript"
    }:

        specific_content = """
node_modules/
dist/
build/
npm-debug.log*
"""

    else:

        specific_content = ""

    content = (
        common_content
        + specific_content
    )

    write_file(
        os.path.join(
            project_dir,
            ".gitignore"
        ),
        content
    )


def generate_pipeline(
    project_dir: str,
    gap_report: dict,
    spec
):

    platform = gap_report[
        "selected_ci_cd_platform"
    ]

    if platform == "azure_devops":

        return generate_azure_pipeline(
            project_dir,
            spec
        )

    if platform == "github_actions":

        return generate_github_actions_pipeline(
            project_dir,
            spec
        )

    if platform == "jenkins":

        return generate_jenkins_pipeline(
            project_dir,
            spec
        )

    if platform == "gitlab_ci":

        return generate_gitlab_pipeline(
            project_dir,
            spec
        )

    raise ValueError(
        "Unsupported CI/CD platform: "
        f"{platform}"
    )


def get_build_commands(
    language: str,
    build_tool: str
) -> dict:

    language = language.lower()
    build_tool = build_tool.lower()

    if language == "python":

        return {
            "install": (
                "python -m pip install "
                "-r requirements.txt"
            ),
            "build": (
                'echo "No compilation '
                'required for Python"'
            ),
            "validate": (
                "python -m compileall ."
            )
        }

    if language == "java":

        if build_tool == "gradle":

            return {
                "install": (
                    'echo "Gradle wrapper used"'
                ),
                "build": (
                    "./gradlew build"
                ),
                "validate": (
                    "./gradlew check"
                )
            }

        return {
            "install": (
                'echo "Maven dependencies '
                'resolved during build"'
            ),
            "build": (
                "mvn clean package"
            ),
            "validate": (
                "mvn verify"
            )
        }

    if language in {
        "node",
        "nodejs",
        "javascript",
        "typescript"
    }:

        return {
            "install": "npm ci",
            "build": "npm run build",
            "validate": "npm test"
        }

    return {
        "install": (
            'echo "Configure dependency '
            'installation"'
        ),
        "build": (
            'echo "Configure build command"'
        ),
        "validate": (
            'echo "Configure validation command"'
        )
    }


def generate_azure_pipeline(
    project_dir: str,
    spec
):

    commands = get_build_commands(
        spec.language,
        spec.build_tool
    )

    content = f"""
trigger:
  branches:
    include:
      - main

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self

  - script: {commands["install"]}
    displayName: Install dependencies

  - script: {commands["validate"]}
    displayName: Validate application

  - script: {commands["build"]}
    displayName: Build application
"""

    pipeline_path = os.path.join(
        project_dir,
        "azure-pipelines.yml"
    )

    write_file(
        pipeline_path,
        content
    )

    return pipeline_path


def generate_github_actions_pipeline(
    project_dir: str,
    spec
):

    commands = get_build_commands(
        spec.language,
        spec.build_tool
    )

    content = f"""
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install dependencies
        run: {commands["install"]}

      - name: Validate application
        run: {commands["validate"]}

      - name: Build application
        run: {commands["build"]}
"""

    pipeline_path = os.path.join(
        project_dir,
        ".github",
        "workflows",
        "ci.yml"
    )

    write_file(
        pipeline_path,
        content
    )

    return pipeline_path


def generate_jenkins_pipeline(
    project_dir: str,
    spec
):

    commands = get_build_commands(
        spec.language,
        spec.build_tool
    )

    content = f"""
pipeline {{
    agent any

    stages {{
        stage('Install dependencies') {{
            steps {{
                sh '{commands["install"]}'
            }}
        }}

        stage('Validate') {{
            steps {{
                sh '{commands["validate"]}'
            }}
        }}

        stage('Build') {{
            steps {{
                sh '{commands["build"]}'
            }}
        }}
    }}
}}
"""

    pipeline_path = os.path.join(
        project_dir,
        "Jenkinsfile"
    )

    write_file(
        pipeline_path,
        content
    )

    return pipeline_path


def generate_gitlab_pipeline(
    project_dir: str,
    spec
):

    commands = get_build_commands(
        spec.language,
        spec.build_tool
    )

    content = f"""
stages:
  - install
  - validate
  - build

install:
  stage: install
  script:
    - {commands["install"]}

validate:
  stage: validate
  script:
    - {commands["validate"]}

build:
  stage: build
  script:
    - {commands["build"]}
"""

    pipeline_path = os.path.join(
        project_dir,
        ".gitlab-ci.yml"
    )

    write_file(
        pipeline_path,
        content
    )

    return pipeline_path