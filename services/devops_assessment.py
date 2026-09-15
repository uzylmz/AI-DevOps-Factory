def compute_devops_score(assets):

    score = 0

    if assets["dockerfile"]:
        score += 25

    if assets["docker_compose"]:
        score += 25

    if assets["azure_pipeline"]:
        score += 25

    if assets["gitignore"]:
        score += 25

    return score


def get_maturity_level(score):

    if score < 25:
        return "Beginner"

    if score < 50:
        return "Basic"

    if score < 75:
        return "Intermediate"

    return "Advanced"