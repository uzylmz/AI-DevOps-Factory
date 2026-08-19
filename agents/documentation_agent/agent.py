import os


def generate_documentation(spec):

    project_dir = f"generated_projects/{spec.project_name}"

    docs_dir = os.path.join(project_dir, "docs")

    os.makedirs(docs_dir, exist_ok=True)

    architecture_content = f"""
# Architecture

## Backend
{spec.backend}

## Database
{spec.database}

## Cloud
{spec.cloud}
"""

    installation_content = f"""
# Installation

## Prérequis

- Docker
- Git

## Lancement

docker-compose up -d
"""

    runbook_content = f"""
# Runbook

## Environnements

{', '.join(spec.environments)}

## Tests disponibles

{', '.join(spec.tests)}
"""

    with open(os.path.join(docs_dir, "architecture.md"), "w") as f:
        f.write(architecture_content)

    with open(os.path.join(docs_dir, "installation.md"), "w") as f:
        f.write(installation_content)

    with open(os.path.join(docs_dir, "runbook.md"), "w") as f:
        f.write(runbook_content)

    print("Documentation generated")