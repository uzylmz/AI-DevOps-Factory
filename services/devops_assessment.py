def compute_devops_score(assets):

    score = 0

    if assets["dockerfile"]:
        score += 20

    if assets["docker_compose"]:
        score += 20

    if assets["azure_pipeline"]:
        score += 20

    if assets["gitignore"]:
        score += 20

    if assets["github_actions"]:
        score += 20

    if assets["kubernetes"]:
        score += 20

    if assets["terraform"]:
        score += 20

    return score


def get_maturity_level(score):

    if score < 40:
        return "Beginner"

    if score < 80:
        return "Basic"

    if score < 120:
        return "Intermediate"

    return "Advanced"