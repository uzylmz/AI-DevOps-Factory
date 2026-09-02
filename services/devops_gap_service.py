from agents.repository_analyzer_agent.existing_devops_detector import (
    detect_existing_devops_assets
)

from agents.repository_analyzer_agent.gap_analyzer import (
    analyze_devops_gaps
)


def get_devops_gap_report(project_path):

    assets = detect_existing_devops_assets(
        project_path
    )

    gaps = analyze_devops_gaps(
        assets
    )

    return {
        "assets": assets,
        "gaps": gaps
    }