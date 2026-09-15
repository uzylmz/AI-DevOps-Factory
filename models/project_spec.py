from pydantic import BaseModel
from typing import List


class ProjectSpec(BaseModel):

    project_name: str

    language: str
    framework: str

    database: str
    build_tool: str

    cloud: str

    environments: List[str]

    docker: bool = True
    ci_cd: bool = True
    kubernetes: bool = False
    terraform: bool = False

    docker_existing: bool = False

    pipeline_existing: bool = False

    git_existing: bool = False