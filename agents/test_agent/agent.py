
from agents.test_agent.playwright_generator import generate_playwright
from agents.test_agent.pytest_generator import generate_pytest


def generate_tests(spec):

    project_dir = f"generated_projects/{spec.project_name}"

    if "playwright" in spec.tests:
        generate_playwright(project_dir)

    if "pytest" in spec.tests:
        generate_pytest(project_dir)

    print("Test generation completed")