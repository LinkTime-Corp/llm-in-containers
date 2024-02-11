import os, json, io, sys
import streamlit as st
from constants import LOCAL_LLM, GPT_LLM
from db_engine import DBEngine
from query_engine import SQLEngineWrapper


script_dir = os.path.dirname(os.path.realpath(__file__))
upper_dir = os.path.dirname(script_dir)
config_path = os.path.join(f"{upper_dir}/conf", "config.json")
with open(config_path) as f:
    config = json.load(f)
    SHOW_TRACE_ON_UI = config["SHOW_TRACE_ON_UI"]

class OutputCapture:
    def __init__(self):
        self.buffer = io.StringIO()

    def isatty(self):
        return False

    def write(self, message):
        self.buffer.write(message)

    def flush(self):
        pass

    def get_output(self):
        return self.buffer.getvalue()

def main():
    st.title("💬 Text2SQL Demo")
    st.sidebar.title("Inference Traces")

    query_engine = SQLEngineWrapper()
    db_engine = DBEngine()

    with st.expander("🐬 DATABASE Information", False):
        col1, col2 = st.columns([1, 2])
        # show all the table names in col1 and show table schema in col2
        # after user selects a table name
        with col1:
            table_names = db_engine.get_table_names()
            table_name = st.selectbox("Select a table", table_names)
        with col2:
            #table_schema = db_engine.get_table_schema(table_name)
            #st.write(table_schema)
            st.dataframe(db_engine.get_table_sample(table_name))

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            else:
                st.code(message["content"])

    llm_type = st.selectbox("LLM Type", [GPT_LLM, LOCAL_LLM])
    debug_info = st.sidebar.empty()
    if prompt := st.chat_input("where is address of the office in San Francisco?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            result = None
            try:
                if SHOW_TRACE_ON_UI:
                    captured_output = OutputCapture()
                    sys.stdout = captured_output

                result = query_engine.process_query(prompt, llm_type)

                if SHOW_TRACE_ON_UI:
                    sys.stdout = sys.__stdout__

                if SHOW_TRACE_ON_UI and captured_output is not None:
                    captured_output_str = captured_output.get_output()
                    debug_info.text_area("", captured_output_str, height=600)
            except Exception as e:
                result = str(e)
            st.write(result)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result,
            }
        )

if __name__ == "__main__":
    main()