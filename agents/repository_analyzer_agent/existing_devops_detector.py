import os


def detect_existing_devops_assets(project_path):

    return {

        "dockerfile": os.path.exists(
            os.path.join(project_path, "Dockerfile")
        ),

        "docker_compose": os.path.exists(
            os.path.join(project_path, "docker-compose.yml")
        ),

        "readme": os.path.exists(
            os.path.join(project_path, "README.md")
        ),

        "azure_pipeline": os.path.exists(
            os.path.join(
                project_path,
                "azure-pipelines.yml"
            )
        ),

        "gitignore": os.path.exists(
            os.path.join(project_path, ".gitignore")
        ),

        "github_actions": os.path.exists(
            os.path.join(
                project_path,
                ".github",
                "workflows"
            )
        ),

        "kubernetes": os.path.exists(
            os.path.join(
                project_path,
                "kubernetes"
            )
        ),

        "terraform": has_terraform_files(
            project_path
        )

    }

import os


def has_terraform_files(project_path):

    for root, dirs, files in os.walk(project_path):

        for file in files:

            if file.endswith(".tf"):
                return True

    return False