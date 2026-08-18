from agents.architect_agent.agent import analyze_project
from agents.devops_agent.agent import generate_project_structure

user_prompt = """
Je veux une application Spring Boot avec PostgreSQL sur Azure
"""

specification = analyze_project(user_prompt)

print(specification.model_dump())

project_path = generate_project_structure("demo-app")

print(f"Projet généré : {project_path}")