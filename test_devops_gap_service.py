from services.devops_gap_service import (
    get_devops_gap_report
)

project_path = r"C:\Users\Uzeyir.YILMAZ\Projets\TAIE_13Aout"

report = get_devops_gap_report(
    project_path
)

print(report)