import streamlit as st
import pandas as pd
from pipeline.query_pipeline import run_query
from pathlib import Path

def render_chat():
    st.title("🤖 Text2SQL Assistant")
    st.caption("Ask questions about your uploaded data.")

    # Initialize memory
    if "history" not in st.session_state:
        st.session_state.history = ""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sql" in message and message["sql"]:
                with st.expander("Generated SQL", expanded=False):
                    st.code(message["sql"], language="sql")
            if "results" in message and message["results"] is not None:
                with st.expander("Results", expanded=False):
                    st.dataframe(message["results"])
            if "chart" in message and message["chart"] is not None:
                st.plotly_chart(message["chart"], width='stretch')

    prompt = st.chat_input("Ask anything...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not st.session_state.get("dataset_loaded"):
            response = "Please upload a dataset first."
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            db_name = Path(st.session_state.dataset_name).stem
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = run_query(db_name, prompt, st.session_state.history)
                
                with st.expander("Retrieved Context", expanded=False):
                    st.markdown(result["context"])
                    
                with st.expander("Generated SQL", expanded=False):
                    st.code(result["sql_query"], language="sql")
                    st.caption(f"Execution Time: {result['exec_result'].execution_time_ms:.2f} ms | Rows: {result['exec_result'].row_count}")
                    
                df_results = None
                if result['exec_result'].row_count > 0:
                    df_results = pd.DataFrame(result['exec_result'].rows, columns=result['exec_result'].columns)
                    with st.expander("Results", expanded=False):
                        st.dataframe(df_results)
                        
                if result["chart"]:
                    st.plotly_chart(result["chart"], width='stretch')
                
                st.markdown("### Answer")
                response_content = st.write_stream(result["answer_generator"])
                
                # Update history
                st.session_state.history += f"\nUser: {prompt}\nAssistant: {response_content}\n"
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_content,
                    "sql": result["sql_query"],
                    "results": df_results,
                    "chart": result["chart"]
                })