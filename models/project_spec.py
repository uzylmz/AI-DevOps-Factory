from pydantic import BaseModel
from typing import List


class ProjectSpec(BaseModel):
    project_name: str
    backend: str
    database: str
    cloud: str
    tests: List[str] = []
    environments: List[str] = []