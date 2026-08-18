from pydantic import BaseModel

class ProjectSpec(BaseModel):
    backend: str
    database: str
    cloud: str