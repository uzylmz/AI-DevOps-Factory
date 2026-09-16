from services.project_spec_builder import (
    build_project_spec_from_repository
)

from services.devops_gap_service import (
    get_devops_gap_report
)

from services.report_generator import (
    generate_devops_report
)

from services.roadmap_generator import (
    generate_devops_roadmap
)

from services.roadmap_report_generator import (
    generate_roadmap_report
)

from services.devops_consultant import (
    generate_executive_summary
)

from agents.lead_agent.agent import (
    execute_project_generation
)


project_path = (
    r"C:\Users\Uzeyir.YILMAZ"
    r"\Projets\LaToile"
)

target_ci_cd_platform = "jenkins"

delivery_method = "source_code"


specification = (
    build_project_spec_from_repository(
        project_path
    )
)


gap_report = get_devops_gap_report(
    project_path,
    target_ci_cd_platform,
    delivery_method
)


print("ProjectSpec:")
print(specification.model_dump())

print()
print("=== GAP REPORT ===")
print(gap_report)


assessment_report = generate_devops_report(
    specification,
    gap_report
)

print()
print(assessment_report)


roadmap = generate_devops_roadmap(
    gap_report
)

roadmap_report = generate_roadmap_report(
    roadmap
)

print()
print(roadmap_report)


consultant_report = (
    generate_executive_summary(
        specification,
        gap_report
    )
)

print()
print("=== DEVOPS CONSULTANT ===")
print(consultant_report)


generated_project = (
    execute_project_generation(
        specification,
        gap_report,
        project_path
    )
)

print()
print(
    f"Projet généré : {generated_project}"
)