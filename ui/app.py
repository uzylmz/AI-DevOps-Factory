import streamlit as st

from services.project_spec_builder import (
    build_project_spec_from_repository
)

from services.devops_gap_service import (
    get_devops_gap_report
)

from services.report_generator import (
    generate_devops_report
)

from services.roadmap_generator import (
    generate_devops_roadmap
)

from services.roadmap_report_generator import (
    generate_roadmap_report
)

from services.devops_consultant import (
    generate_executive_summary
)


st.set_page_config(
    page_title="AI DevOps Factory",
    layout="wide"
)

st.title("🚀 AI DevOps Factory")

st.markdown(
    "Analyze an existing repository and generate a DevOps assessment."
)

project_path = st.text_input(
    "Repository path",
    value=""
)

if st.button("Analyze Project"):

    if not project_path:

        st.error(
            "Please provide a repository path."
        )

    else:

        with st.spinner(
            "Analyzing repository..."
        ):

            specification = (
                build_project_spec_from_repository(
                    project_path
                )
            )

            gap_report = (
                get_devops_gap_report(
                    project_path
                )
            )

            assessment_report = (
                generate_devops_report(
                    specification,
                    gap_report["assets"],
                    gap_report["gaps"]
                )
            )

            roadmap = generate_devops_roadmap(
                gap_report["gaps"]
            )

            roadmap_report = (
                generate_roadmap_report(
                    roadmap
                )
            )

            consultant_report = (
                generate_executive_summary(
                    specification,
                    gap_report
                )
            )

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "ProjectSpec",
                "Gap Report",
                "Assessment",
                "Roadmap",
                "Consultant"
            ]
        )

        with tab1:

            st.subheader(
                "Project Specification"
            )

            st.json(
                specification.model_dump()
            )

        with tab2:

            st.subheader(
                "Gap Report"
            )

            st.json(
                gap_report
            )

        with tab3:

            st.subheader(
                "DevOps Assessment"
            )

            st.text_area(
                "",
                assessment_report,
                height=500
            )

        with tab4:

            st.subheader(
                "DevOps Roadmap"
            )

            st.text_area(
                "",
                roadmap_report,
                height=500
            )

        with tab5:

            st.subheader(
                "DevOps Consultant"
            )

            st.text_area(
                "",
                consultant_report,
                height=700
            )