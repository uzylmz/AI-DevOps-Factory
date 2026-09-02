def analyze_devops_gaps(devops_assets):

    return {

        "generate_dockerfile":
            not devops_assets["dockerfile"],

        "generate_docker_compose":
            not devops_assets["docker_compose"],

        "generate_readme":
            not devops_assets["readme"],

        "generate_pipeline":
            not devops_assets["azure_pipeline"],

        "generate_gitignore":
            not devops_assets["gitignore"]
    }