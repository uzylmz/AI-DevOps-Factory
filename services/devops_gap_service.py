from agents.repository_analyzer_agent.existing_devops_detector import (
    detect_existing_devops_assets
)

from agents.repository_analyzer_agent.gap_analyzer import (
    analyze_devops_gaps
)


def get_devops_gap_report(
    project_path: str,
    target_ci_cd_platform: str = "azure_devops",
    delivery_method: str = "source_code"
) -> dict:

    assets = detect_existing_devops_assets(
        project_path
    )

    gaps = analyze_devops_gaps(
        assets,
        target_ci_cd_platform,
        delivery_method
    )

    return {
        "selected_ci_cd_platform": (
            target_ci_cd_platform
        ),

        "selected_delivery_method": (
            delivery_method
        ),

        "assets": assets,

        "gaps": gaps
    }