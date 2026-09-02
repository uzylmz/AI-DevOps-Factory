from agents.repository_analyzer_agent.gap_analyzer import (
    analyze_devops_gaps
)

assets = {
    "dockerfile": False,
    "docker_compose": False,
    "readme": True,
    "azure_pipeline": True
}

result = analyze_devops_gaps(assets)

print(result)