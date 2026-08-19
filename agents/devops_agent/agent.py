import os

def generate_project_structure(spec):

    output_dir = f"generated_projects/{spec.project_name}"

    os.makedirs(output_dir, exist_ok=True)

    dockerfile_content = get_dockerfile_content(spec.backend)

    with open(f"{output_dir}/Dockerfile", "w") as f:
        f.write(dockerfile_content)

    with open(f"{output_dir}/README.md", "w") as f:
        f.write(
        f"""
        # {spec.project_name}

        ## Backend
        {spec.backend}

        ## Database
        {spec.database}

        ## Cloud
        {spec.cloud}

        ## Tests
        {', '.join(spec.tests)}

        ## Environments
        {', '.join(spec.environments)}
        """
        )

    return output_dir

def get_dockerfile_content(backend):

    if backend == "springboot":
        return """
FROM eclipse-temurin:21-jdk

WORKDIR /app

COPY . .

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
"""

    elif backend == "python":
        return """
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
"""

    elif backend == "nodejs":
        return """
FROM node:20

WORKDIR /app

COPY . .

RUN npm install

CMD ["npm", "start"]
"""

    return "FROM alpine:latest"

