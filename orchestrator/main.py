from agents.architect_agent.agent import analyze_project
from agents.lead_agent.agent import execute_project_generation

user_prompt = """
Je souhaite créer une API Python.

La base de données doit être PostgreSQL.

Le déploiement doit se faire sur Azure.

Je veux des tests Playwright et Pytest.

Les environnements sont :
- dev
- test
- prod
"""

specification = analyze_project(user_prompt)

print(specification.model_dump())

project_path = execute_project_generation(specification)

print(f"Projet généré : {project_path}")