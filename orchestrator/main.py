from services.project_spec_builder import (
    build_project_spec_from_repository
)

from agents.lead_agent.agent import (
    execute_project_generation
)

from services.devops_gap_service import (
    get_devops_gap_report
)

project_path = r"C:\Users\Uzeyir.YILMAZ\Projets\NodeDemo"

specification = build_project_spec_from_repository(
    project_path
)

target_path = project_path

print("ProjectSpec:")
print(specification.model_dump())

gap_report = get_devops_gap_report(
    project_path
)

print()
print("=== GAP REPORT ===")
print(gap_report)

generated_project = execute_project_generation(
    specification, gap_report, target_path
)

print(f"Projet généré : {generated_project}")