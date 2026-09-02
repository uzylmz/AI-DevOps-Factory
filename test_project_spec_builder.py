from agents.repository_analyzer_agent.project_spec_builder import build_project_spec

analysis_result = {
    "language": "Python",
    "framework": "Flask",
    "database": "PostgreSQL",
    "build_tool": "pip"
}

spec = build_project_spec(analysis_result)

print(spec.model_dump())