from services.devops_options import (
    CI_CD_PLATFORM_ASSET_KEYS
)


def compute_devops_score(
    assets: dict,
    delivery_method: str = "source_code",
    target_ci_cd_platform: str = "azure_devops"
) -> int:

    score = 0
    maximum_score = 0

    maximum_score += 20

    if assets.get(
        "gitignore",
        False
    ):
        score += 20

    maximum_score += 15

    if assets.get(
        "readme",
        False
    ):
        score += 15

    pipeline_asset_key = (
        CI_CD_PLATFORM_ASSET_KEYS.get(
            target_ci_cd_platform
        )
    )

    maximum_score += 30

    if (
        pipeline_asset_key
        and assets.get(
            pipeline_asset_key,
            False
        )
    ):
        score += 30

    if delivery_method == "container_image":

        maximum_score += 20

        if assets.get(
            "dockerfile",
            False
        ):
            score += 20

        maximum_score += 15

        if assets.get(
            "docker_compose",
            False
        ):
            score += 15

    if maximum_score == 0:
        return 0

    return round(
        score * 100 / maximum_score
    )


def get_maturity_level(
    score: int
) -> str:

    if score < 25:
        return "Beginner"

    if score < 50:
        return "Basic"

    if score < 75:
        return "Intermediate"

    return "Advanced"