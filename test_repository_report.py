from agents.repository_analyzer_agent.existing_devops_detector import (
    detect_existing_devops_assets
)

project_path = r"C:\Users\Uzeyir.YILMAZ\Projets\TAIE_13Aout"

result = detect_existing_devops_assets(
    project_path
)

print()

print("=== DEVOPS ASSET REPORT ===")

for key, value in result.items():

    status = "FOUND" if value else "MISSING"

    print(f"{key}: {status}")