def generate_roadmap_report(roadmap):

    report = """
==================================
DEVOPS ROADMAP
==================================
"""

    for item in roadmap:

        report += f"""

Priority {item['priority']}
-------------------------

Task:
{item['task']}

Expected Impact:
{item['impact']}
"""

    return report