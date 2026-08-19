from agents.devops_agent.agent import generate_project_structure
from agents.test_agent.agent import generate_tests
from agents.documentation_agent.agent import generate_documentation


def execute_project_generation(spec):

    print("Starting project generation...")

    project_path = generate_project_structure(spec)

    generate_tests(spec)

    generate_documentation(spec)

    print("Project generation completed")

    return project_path