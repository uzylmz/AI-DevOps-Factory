import os


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode"
}


def file_exists_in_repository(
    project_path: str,
    filename: str
) -> bool:

    expected_filename = filename.lower()

    for root, directories, files in os.walk(
        project_path
    ):

        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for current_file in files:

            if current_file.lower() == expected_filename:
                return True

    return False


def folder_exists_in_repository(
    project_path: str,
    folder_names: list[str]
) -> bool:

    expected_names = {
        name.lower()
        for name in folder_names
    }

    for root, directories, files in os.walk(
        project_path
    ):

        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for directory in directories:

            if directory.lower() in expected_names:
                return True

    return False


def has_github_actions(
    project_path: str
) -> bool:

    workflows_path = os.path.join(
        project_path,
        ".github",
        "workflows"
    )

    if not os.path.isdir(workflows_path):
        return False

    for filename in os.listdir(
        workflows_path
    ):

        if filename.lower().endswith(
            (".yml", ".yaml")
        ):
            return True

    return False


def has_terraform_files(
    project_path: str
) -> bool:

    for root, directories, files in os.walk(
        project_path
    ):

        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for filename in files:

            if filename.lower().endswith(
                ".tf"
            ):
                return True

    return False


def detect_existing_devops_assets(
    project_path: str
) -> dict:

    azure_pipeline = (
        file_exists_in_repository(
            project_path,
            "azure-pipelines.yml"
        )
        or file_exists_in_repository(
            project_path,
            "azure-pipelines.yaml"
        )
    )

    github_actions = has_github_actions(
        project_path
    )

    jenkins_pipeline = (
        file_exists_in_repository(
            project_path,
            "Jenkinsfile"
        )
    )

    gitlab_pipeline = (
        file_exists_in_repository(
            project_path,
            ".gitlab-ci.yml"
        )
    )

    detected_ci_cd_platforms = []

    if azure_pipeline:
        detected_ci_cd_platforms.append(
            "azure_devops"
        )

    if github_actions:
        detected_ci_cd_platforms.append(
            "github_actions"
        )

    if jenkins_pipeline:
        detected_ci_cd_platforms.append(
            "jenkins"
        )

    if gitlab_pipeline:
        detected_ci_cd_platforms.append(
            "gitlab_ci"
        )

    return {
        "dockerfile": (
            file_exists_in_repository(
                project_path,
                "Dockerfile"
            )
        ),

        "docker_compose": (
            file_exists_in_repository(
                project_path,
                "docker-compose.yml"
            )
            or file_exists_in_repository(
                project_path,
                "docker-compose.yaml"
            )
            or file_exists_in_repository(
                project_path,
                "compose.yml"
            )
            or file_exists_in_repository(
                project_path,
                "compose.yaml"
            )
        ),

        "readme": (
            file_exists_in_repository(
                project_path,
                "README.md"
            )
        ),

        "gitignore": (
            file_exists_in_repository(
                project_path,
                ".gitignore"
            )
        ),

        "azure_pipeline": (
            azure_pipeline
        ),

        "github_actions": (
            github_actions
        ),

        "jenkins_pipeline": (
            jenkins_pipeline
        ),

        "gitlab_pipeline": (
            gitlab_pipeline
        ),

        "ci_cd_platforms": (
            detected_ci_cd_platforms
        ),

        "kubernetes": (
            folder_exists_in_repository(
                project_path,
                [
                    "kubernetes",
                    "k8s",
                    "helm",
                    "charts"
                ]
            )
        ),

        "terraform": (
            has_terraform_files(
                project_path
            )
        )
    }