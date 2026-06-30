import streamlit as st

from components.styles import load_css
from components.sidebar import render_sidebar
from components.chat import render_chat

st.set_page_config(
    page_title="Text2SQL AI Agent",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# Initialize session state variables

DEFAULTS = {
    "messages": [],
    "dataset": None,
    "dataset_loaded": False,
    "dataset_name": None,
    "database_path": None,
    "tables": [],
    "ddl": {},
    "profiles": [],
    "status": "Waiting for upload",
}


for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value



if "messages" not in st.session_state:
    st.session_state.messages = []

if "dataset_loaded" not in st.session_state:
    st.session_state.dataset_loaded = False

with st.sidebar:
    render_sidebar()

# Render chat in the main area so the chat_input pins to the bottom of the screen natively
render_chat()