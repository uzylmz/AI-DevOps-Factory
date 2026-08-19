
import os


def generate_pytest(project_dir):

    path = os.path.join(project_dir, "tests", "pytest")

    os.makedirs(path, exist_ok=True)

    content = """
def test_healthcheck():
    assert True
"""

    with open(os.path.join(path, "test_api.py"), "w") as f:
        f.write(content)

    print("Pytest tests generated")