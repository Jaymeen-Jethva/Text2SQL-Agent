import streamlit as st


def load_css():

    st.markdown(
        """
<style>

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
}

.stChatMessage{
    border-radius:12px;
}

</style>
""",
        unsafe_allow_html=True,
    )