from pathlib import Path
import sys

import streamlit as st


# Permet à Streamlit de trouver les modules du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from agents.lead_agent.agent import (
    execute_project_generation
)

from services.project_spec_builder import (
    build_project_spec_from_repository
)

from services.devops_gap_service import (
    get_devops_gap_report
)

from services.devops_assessment import (
    compute_devops_score,
    get_maturity_level
)

from services.report_generator import (
    generate_devops_report
)

from services.roadmap_generator import (
    generate_devops_roadmap
)

from services.devops_options import (
    CI_CD_PLATFORM_OPTIONS,
    CI_CD_PLATFORM_DISPLAY_NAMES,
    CI_CD_PLATFORM_ASSET_KEYS,
    DELIVERY_METHOD_OPTIONS,
    DELIVERY_METHOD_DISPLAY_NAMES
)


# ---------------------------------------------------------
# Configuration Streamlit
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI DevOps Factory",
    page_icon="⚙️",
    layout="wide"
)


# ---------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------

def initialize_session_state():

    default_values = {
        "analysis_completed": False,
        "specification": None,
        "gap_report": None,
        "assessment_report": None,
        "roadmap": None,
        "score": None,
        "maturity": None,
        "analyzed_project_path": None
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_analysis():

    st.session_state.analysis_completed = False
    st.session_state.specification = None
    st.session_state.gap_report = None
    st.session_state.assessment_report = None
    st.session_state.roadmap = None
    st.session_state.score = None
    st.session_state.maturity = None
    st.session_state.analyzed_project_path = None


def validate_project_path(project_path: str):

    if not project_path.strip():
        return False, "Veuillez saisir le chemin d'un projet."

    path = Path(project_path).expanduser()

    if not path.exists():
        return False, "Le chemin indiqué n'existe pas."

    if not path.is_dir():
        return False, "Le chemin doit correspondre à un dossier."

    return True, ""


def display_asset_status(
    label: str,
    present: bool
):

    if present:
        st.success(f"{label}: Present")
    else:
        st.warning(f"{label}: Missing")


def get_selected_value(
    display_value: str,
    options: dict
):

    return options[display_value]


# ---------------------------------------------------------
# Initialisation
# ---------------------------------------------------------

initialize_session_state()


# ---------------------------------------------------------
# En-tête
# ---------------------------------------------------------

st.title("⚙️ AI DevOps Factory")

st.write(
    """
Analysez un projet existant, identifiez les éléments DevOps
présents ou manquants, obtenez un score de maturité et générez
uniquement les composants nécessaires.
"""
)


# ---------------------------------------------------------
# Barre latérale
# ---------------------------------------------------------

with st.sidebar:

    st.header("Configuration")

    selected_platform_label = st.selectbox(
        "CI/CD Platform",
        options=list(
            CI_CD_PLATFORM_OPTIONS.keys()
        ),
        index=0
    )

    selected_delivery_label = st.selectbox(
        "Delivery Method",
        options=list(
            DELIVERY_METHOD_OPTIONS.keys()
        ),
        index=0
    )

    selected_platform = get_selected_value(
        selected_platform_label,
        CI_CD_PLATFORM_OPTIONS
    )

    selected_delivery_method = get_selected_value(
        selected_delivery_label,
        DELIVERY_METHOD_OPTIONS
    )

    st.divider()

    st.subheader("Selected configuration")

    st.write(
        f"CI/CD: {selected_platform_label}"
    )

    st.write(
        f"Delivery: {selected_delivery_label}"
    )

    st.divider()

    if st.button(
        "Reset analysis",
        width="stretch"
    ):
        reset_analysis()
        st.rerun()


# ---------------------------------------------------------
# Sélection du projet
# ---------------------------------------------------------

st.subheader("1. Select an existing project")

project_path = st.text_input(
    "Project directory",
    placeholder=(
        r"C:\Users\YourName\Projects\MyProject"
    ),
    help=(
        "Indiquez le chemin absolu du projet "
        "que vous souhaitez analyser."
    )
)


analyze_button = st.button(
    "🔍 Analyze project",
    type="primary",
    width="stretch"
)


# ---------------------------------------------------------
# Analyse du projet
# ---------------------------------------------------------

if analyze_button:

    is_valid, error_message = validate_project_path(
        project_path
    )

    if not is_valid:
        st.error(error_message)

    else:

        normalized_project_path = str(
            Path(project_path).resolve()
        )

        try:

            with st.spinner(
                "Repository analysis in progress..."
            ):

                specification = (
                    build_project_spec_from_repository(
                        normalized_project_path
                    )
                )

                
                gap_report = get_devops_gap_report(
                    normalized_project_path,
                    target_ci_cd_platform=(
                        selected_platform
                    ),
                    delivery_method=(
                        selected_delivery_method
                    )
                )
    
                score = compute_devops_score(
                    gap_report["assets"],
                    selected_delivery_method,
                    selected_platform
                )

                maturity = get_maturity_level(
                    score
                )

                assessment_report = (
                    generate_devops_report(
                        specification,
                        gap_report
                    )
                )

                roadmap = generate_devops_roadmap(
                    gap_report
                )

            st.session_state.specification = (
                specification
            )

            st.session_state.gap_report = (
                gap_report
            )

            st.session_state.score = score

            st.session_state.maturity = maturity

            st.session_state.assessment_report = (
                assessment_report
            )

            st.session_state.roadmap = roadmap

            st.session_state.analyzed_project_path = (
                normalized_project_path
            )

            st.session_state.analysis_completed = True

            st.success(
                "Project analysis completed successfully."
            )

        except Exception as error:

            st.session_state.analysis_completed = False

            st.error(
                "The project analysis failed."
            )

            st.exception(error)


# ---------------------------------------------------------
# Affichage des résultats
# ---------------------------------------------------------

if st.session_state.analysis_completed:

    specification = (
        st.session_state.specification
    )

    gap_report = (
        st.session_state.gap_report
    )

    assets = gap_report["assets"]

    score = st.session_state.score

    maturity = st.session_state.maturity

    assessment_report = (
        st.session_state.assessment_report
    )

    roadmap = st.session_state.roadmap

    analyzed_project_path = (
        st.session_state.analyzed_project_path
    )

    platform = gap_report[
        "selected_ci_cd_platform"
    ]

    delivery_method = gap_report[
        "selected_delivery_method"
    ]

    platform_label = (
        CI_CD_PLATFORM_DISPLAY_NAMES.get(
            platform,
            platform
        )
    )

    delivery_label = (
        DELIVERY_METHOD_DISPLAY_NAMES.get(
            delivery_method,
            delivery_method
        )
    )

    detected_platforms = assets.get(
    "ci_cd_platforms",
    []
    )

    detected_platform_labels = [
        CI_CD_PLATFORM_DISPLAY_NAMES.get(
            item,
            item
        )
        for item in detected_platforms
    ]

    st.subheader(
        "Detected Platform"
    )

    if detected_platform_labels:

        st.success(
            "Detected CI/CD Platform(s): "
            + ", ".join(
                detected_platform_labels
            )
        )

    else:

        st.warning(
            "No CI/CD platform detected."
        )

    if assets.get(
        "dockerfile",
        False
    ):

        st.success(
            "Detected Delivery Method: "
            "Container Image"
        )

    else:

        st.info(
            "Detected Delivery Method: "
            "Source Code"
        )

    if detected_platforms:

        if platform in detected_platforms:

            st.success(
                f"Selected platform ({platform_label}) "
                "matches the detected platform."
            )

        else:

            st.warning(
                f"Selected platform ({platform_label}) "
                "differs from the detected platform(s): "
                f"{', '.join(detected_platform_labels)}"
            )

    st.divider()

    st.subheader("2. Project analysis")

    project_col1, project_col2 = st.columns(2)

    with project_col1:

        st.info(
            f"Project: {specification.project_name}"
        )

        st.write(
            f"Language: `{specification.language}`"
        )

        st.write(
            f"Framework: `{specification.framework}`"
        )

        st.write(
            f"Database: "
            f"`{specification.database or 'unknown'}`"
        )

    with project_col2:

        st.info(
            f"Build tool: "
            f"{specification.build_tool or 'unknown'}"
        )

        st.write(
            f"CI/CD platform: `{platform_label}`"
        )

        st.write(
            f"Delivery method: `{delivery_label}`"
        )

        st.write(
            f"Project path: `{analyzed_project_path}`"
        )

    st.divider()

    st.subheader("3. DevOps maturity")

    metric_col1, metric_col2, metric_col3 = (
        st.columns(3)
    )

    with metric_col1:

        st.metric(
            label="DevOps Score",
            value=f"{score}/100"
        )

    with metric_col2:

        st.metric(
            label="Maturity Level",
            value=maturity
        )

    with metric_col3:

        missing_asset_count = sum(
            1
            for value in gap_report["gaps"].values()
            if value
        )

        st.metric(
            label="Missing Assets",
            value=missing_asset_count
        )

    st.progress(
        score / 100,
        text=f"DevOps maturity: {score}%"
    )

    st.divider()

    st.subheader("4. Existing DevOps assets")

    assets_col1, assets_col2 = st.columns(2)

    with assets_col1:

        display_asset_status(
            "README",
            assets.get("readme", False)
        )

        display_asset_status(
            ".gitignore",
            assets.get("gitignore", False)
        )

        if delivery_method == "container_image":

            display_asset_status(
                "Dockerfile",
                assets.get(
                    "dockerfile",
                    False
                )
            )

            display_asset_status(
                "Docker Compose",
                assets.get(
                    "docker_compose",
                    False
                )
            )

        else:

            st.info(
                "Containerization assets are not required "
                "for the selected delivery method."
            )

    with assets_col2:

        platform = gap_report[
            "selected_ci_cd_platform"
        ]

        pipeline_asset_key = (
            CI_CD_PLATFORM_ASSET_KEYS.get(
                platform
            )
        )

        pipeline_label = (
            CI_CD_PLATFORM_DISPLAY_NAMES.get(
                platform,
                platform
            )
        )

        display_asset_status(
            f"{pipeline_label} Pipeline",
            assets.get(
                pipeline_asset_key,
                False
            )
        )

        display_asset_status(
            "Kubernetes",
            assets.get(
                "kubernetes",
                False
            )
        )

        display_asset_status(
            "Terraform",
            assets.get(
                "terraform",
                False
            )
        )

    st.divider()

    st.subheader("5. Recommended roadmap")

    if roadmap:

        roadmap_rows = []

        for item in roadmap:

            roadmap_rows.append({
                "Priority": item["priority"],
                "Task": item["task"],
                "Expected Impact": item["impact"]
            })

        st.dataframe(
            roadmap_rows,
            width="stretch",
            hide_index=True
        )

    else:

        st.success(
            "No basic DevOps remediation is required."
        )

    st.divider()

    st.subheader("6. Full assessment report")

    with st.expander(
        "Open the assessment report",
        expanded=False
    ):

        st.code(
            assessment_report,
            language="text"
        )

        st.download_button(
            label="Download report",
            data=assessment_report,
            file_name=(
                f"{specification.project_name}"
                "-devops-assessment.txt"
            ),
            mime="text/plain"
        )

    st.divider()

    st.subheader("7. Generate missing DevOps assets")

    st.warning(
        "The generated files will be written directly "
        "into the analyzed project directory. "
        "Existing detected files should not be overwritten."
    )

    generation_enabled = any(
        gap_report["gaps"].values()
    )

    generate_button = st.button(
        "🛠️ Generate missing assets",
        type="primary",
        disabled=not generation_enabled,
        width="stretch"
    )

    if not generation_enabled:

        st.success(
            "All required basic DevOps assets are already present."
        )

    if generate_button:

        try:

            with st.spinner(
                "Generating missing DevOps assets..."
            ):

                generated_project_path = (
                    execute_project_generation(
                        specification,
                        gap_report,
                        analyzed_project_path
                    )
                )

            st.success(
                "Missing DevOps assets generated "
                "successfully."
            )

            st.write(
                f"Output path: "
                f"`{generated_project_path}`"
            )

            refreshed_gap_report = (
                get_devops_gap_report(
                    analyzed_project_path,
                    target_ci_cd_platform=(
                        platform
                    ),
                    delivery_method=(
                        delivery_method
                    )
                )
            )

            st.session_state.gap_report = (
                refreshed_gap_report
            )

            refreshed_score = compute_devops_score(
                refreshed_gap_report["assets"],
                delivery_method,
                platform
            )

            st.session_state.score = (
                refreshed_score
            )

            st.session_state.maturity = (
                get_maturity_level(
                    refreshed_score
                )
            )

            st.session_state.assessment_report = (
                generate_devops_report(
                    specification,
                    refreshed_gap_report
                )
            )

            st.session_state.roadmap = (
                generate_devops_roadmap(
                    refreshed_gap_report
                )
            )

            st.info(
                "The assessment has been refreshed. "
                "Rerun or refresh the page to display "
                "the updated results."
            )

        except Exception as error:

            st.error(
                "The DevOps asset generation failed."
            )

            st.exception(error)