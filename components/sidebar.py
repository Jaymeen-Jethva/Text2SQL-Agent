import streamlit as st

from pipeline.ingestion_pipeline import run_pipeline
from utils.sql_utils import list_tables


def render_sidebar():

    with st.sidebar:

        st.title("📂 Dataset")

        uploaded_file = st.file_uploader(
            "Upload Dataset",
            type=["csv", "xlsx", "xls"],
        )

        # ---------------------------------
        # Process uploaded file
        # ---------------------------------

        if uploaded_file is not None:

            # Prevent processing the same file repeatedly
            if (
                not st.session_state.dataset_loaded
                or st.session_state.dataset_name != uploaded_file.name
            ):

                with st.spinner("Processing dataset..."):

                    result = run_pipeline(uploaded_file)

                st.session_state.dataset = result["dataset"]
                st.session_state.database_path = result["db_path"]
                st.session_state.tables = result["tables"]
                st.session_state.dataset_name = result["dataset_name"]
                st.session_state.dataset_loaded = True
                st.session_state.status = "SQLite Ready"

        # ---------------------------------
        # Dataset Preview
        # ---------------------------------

        if st.session_state.dataset_loaded:

            st.divider()

            st.subheader("Preview")

            first_table = next(
                iter(st.session_state.dataset["tables"])
            )

            df = st.session_state.dataset["tables"][first_table]

            st.dataframe(
                df.head(),
                use_container_width=True,
                height=220,
            )

        # ---------------------------------
        # SQLite Tables
        # ---------------------------------

        if (
            st.session_state.dataset_loaded
            and "database_path" in st.session_state
        ):

            sqlite_tables = list_tables(
                st.session_state.database_path
            )

            st.divider()

            st.subheader("SQLite Tables")

            for table in sqlite_tables:
                st.success(table)

        # ---------------------------------
        # Semantic Layer
        # ---------------------------------

        st.divider()

        st.subheader("Semantic Layer")

        st.button(
            "Generate Semantic Layer",
            use_container_width=True,
            type="primary",
        )

        # ---------------------------------
        # Status
        # ---------------------------------

        st.divider()

        st.subheader("Status")

        st.info(st.session_state.status)

        # ---------------------------------
        # Dataset Tables
        # ---------------------------------

        st.divider()

        st.subheader("Loaded Tables")

        if len(st.session_state.tables) == 0:

            st.caption("No tables loaded.")

        else:

            for table in st.session_state.tables:

                st.success(table)