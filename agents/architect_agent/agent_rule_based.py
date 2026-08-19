from models.project_spec import ProjectSpec


def analyze_project(prompt: str):

    prompt = prompt.lower()

    backend = "unknown"

    if "spring" in prompt:
        backend = "springboot"

    elif "python" in prompt:
        backend = "python"

    elif "node" in prompt:
        backend = "nodejs"

    database = "unknown"

    if "postgres" in prompt:
        database = "postgresql"

    cloud = "unknown"

    if "azure" in prompt:
        cloud = "azure"

    tests = []

    if "playwright" in prompt:
        tests.append("playwright")

    if "pytest" in prompt:
        tests.append("pytest")

    environments = ["dev"]

    if "test" in prompt:
        environments.append("test")

    if "prod" in prompt:
        environments.append("prod")

    return ProjectSpec(
        project_name="demo-app",
        backend=backend,
        database=database,
        cloud=cloud,
        tests=tests,
        environments=environments
    )