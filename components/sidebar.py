import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("📂 Dataset")

        uploaded_file = st.file_uploader(
            "Upload Dataset",
            type=["csv","xlsx","xls"]
        )

        if uploaded_file is not None:

            from service.upload_service import save_uploaded_file
            from service.dataframe_service import load_dataset

            local_path = save_uploaded_file(uploaded_file)

            dataset = load_dataset(local_path)

            st.session_state.dataset_loaded = True

            st.session_state.dataset_name = uploaded_file.name

            st.session_state.tables = list(
                dataset["tables"].keys()
            )

            st.session_state.dataset = dataset

            st.session_state.status = "Dataset Loaded"

        
        
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

        st.divider()

        st.subheader("Semantic Layer")

        st.button(
            "Generate",
            use_container_width=True,
            type="primary",
        )

        st.divider()

        st.subheader("Status")

        st.info(st.session_state.status)

        st.divider()

        st.subheader("Tables")

        if len(st.session_state.tables) == 0:

            st.caption("No tables loaded.")

        else:

            for table in st.session_state.tables:

                st.success(table)