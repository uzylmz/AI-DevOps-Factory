from agents.repository_analyzer_agent.existing_devops_detector import (
    detect_existing_devops_assets
)

project_path = r"C:\Users\Uzeyir.YILMAZ\Projets\LaToile"

result = detect_existing_devops_assets(
    project_path
)

print(result)