from agents.devops_agent.agent import generate_project_structure
from agents.documentation_agent.agent import generate_documentation


def execute_project_generation(spec, gap_report, target_path):

    print("Starting project generation...")

    project_path = generate_project_structure(spec, gap_report, target_path)

    generate_documentation(spec)

    print("Project generation completed")

    return project_path