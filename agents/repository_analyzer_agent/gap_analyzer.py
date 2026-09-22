from services.devops_options import (
    CI_CD_PLATFORM_ASSET_KEYS
)


def analyze_devops_gaps(
    devops_assets: dict,
    target_ci_cd_platform: str = "azure_devops",
    delivery_method: str = "source_code"
) -> dict:

    pipeline_asset_key = (
        CI_CD_PLATFORM_ASSET_KEYS.get(
            target_ci_cd_platform
        )
    )

    if pipeline_asset_key is None:

        supported_platforms = ", ".join(
            CI_CD_PLATFORM_ASSET_KEYS.keys()
        )

        raise ValueError(
            "Unsupported CI/CD platform: "
            f"{target_ci_cd_platform}. "
            "Supported platforms: "
            f"{supported_platforms}"
        )

    if delivery_method not in {
        "source_code",
        "container_image"
    }:

        raise ValueError(
            "Unsupported delivery method: "
            f"{delivery_method}"
        )

    selected_pipeline_exists = (
        devops_assets.get(
            pipeline_asset_key,
            False
        )
    )

    container_delivery = (
        delivery_method == "container_image"
    )

    return {
        "generate_dockerfile": (
            container_delivery
            and not devops_assets.get(
                "dockerfile",
                False
            )
        ),

        "generate_docker_compose": (
            container_delivery
            and not devops_assets.get(
                "docker_compose",
                False
            )
        ),

        "generate_readme": (
            not devops_assets.get(
                "readme",
                False
            )
        ),

        "generate_pipeline": (
            not selected_pipeline_exists
        ),

        "generate_gitignore": (
            not devops_assets.get(
                "gitignore",
                False
            )
        )
    }