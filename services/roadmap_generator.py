def generate_devops_roadmap(gaps):

    roadmap = []

    priority = 1

    if gaps["generate_dockerfile"]:

        roadmap.append({
            "priority": priority,
            "task": "Generate Dockerfile",
            "impact": "Containerization"
        })

        priority += 1

    if gaps["generate_docker_compose"]:

        roadmap.append({
            "priority": priority,
            "task": "Generate docker-compose.yml",
            "impact": "Local orchestration"
        })

        priority += 1

    if gaps["generate_pipeline"]:

        roadmap.append({
            "priority": priority,
            "task": "Generate Azure Pipeline",
            "impact": "CI/CD"
        })

        priority += 1

    if gaps["generate_readme"]:

        roadmap.append({
            "priority": priority,
            "task": "Generate README",
            "impact": "Documentation"
        })

    return roadmap