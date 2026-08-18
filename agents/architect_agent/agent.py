from models.project_spec import ProjectSpec

def analyze_project(prompt: str):

    return ProjectSpec(
        backend="springboot",
        database="postgresql",
        cloud="azure"
    )