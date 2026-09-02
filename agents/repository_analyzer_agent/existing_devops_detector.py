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
        )
    }