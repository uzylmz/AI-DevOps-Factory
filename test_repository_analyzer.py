from agents.repository_analyzer_agent.agent import analyze_repository

result = analyze_repository(
    r"C:\Users\Uzeyir.YILMAZ\Projets\TAIE_13Aout"
)

print(result)

from agents.repository_analyzer_agent.agent import (
    analyze_repository_with_llm
)

result = analyze_repository_with_llm(
    r"C:\Users\Uzeyir.YILMAZ\Projets\TAIE_13Aout"
)

print(result)