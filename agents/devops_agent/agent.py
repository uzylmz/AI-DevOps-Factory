import os

def generate_project_structure(project_name):

    output_dir = f"generated_projects/{project_name}"

    os.makedirs(output_dir, exist_ok=True)

    # Dockerfile
    with open(f"{output_dir}/Dockerfile", "w") as f:
        f.write("FROM eclipse-temurin:21-jdk\n")

    # docker-compose
    with open(f"{output_dir}/docker-compose.yml", "w") as f:
        f.write(
"""services:
  app:
    build: .
    ports:
      - "8080:8080"
"""
        )

    # README
    with open(f"{output_dir}/README.md", "w") as f:
        f.write(f"# {project_name}\n")

    # Gitignore
    with open(f"{output_dir}/.gitignore", "w") as f:
        f.write(".idea/\n.vscode/\n")

    return output_dir