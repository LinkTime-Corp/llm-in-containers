import pandas as pd
import streamlit as st
import json, io, os, shutil, sys, traceback
from constants import TEXT2SQL_ENGINE, CHAINOFTABLE_ENGINE, GPT_LLM, LOCAL_LLM
from llama_index.llama_pack import download_llama_pack

def init_llama_packs():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pack_list = [
        { 
            "name": "ChainOfTablePack", 
            "dir":  "chain_of_table_pack"
        },{
            "name": "MixSelfConsistencyPack",
            "dir": "mix_self_consistency_pack"
        }
    ]
    for pack in pack_list:
        pack_dir  = pack["dir"]
        pack_name = pack["name"]
        pack_path = f"{dir_path}/{pack_dir}"
        if not os.path.exists(pack_path):
            download_llama_pack(
                pack_name,
                pack_path,
                skip_load=True,
            )
init_llama_packs()
from backend import QueryEngineWrapper

script_dir = os.path.dirname(os.path.realpath(__file__))
upper_dir = os.path.dirname(script_dir)
config_path = os.path.join(f"{upper_dir}/conf", "config.json")
with open(config_path) as f:
    config = json.load(f)
    INPUT_DIR = config["INPUT_DIR"]
    SHOW_TRACE_ON_UI = config["SHOW_TRACE_ON_UI"]

wrapper = QueryEngineWrapper()

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

def check_dirs():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
    else:
        shutil.rmtree(INPUT_DIR)
        os.makedirs(INPUT_DIR)

def process_cvs(csv_file):
    check_dirs()
    # save the uploaded file to a directory with the same name
    filepath = f"{INPUT_DIR}/{csv_file.name}"
    with open(filepath, "wb") as f:
        f.write(csv_file.getbuffer())
    return pd.read_csv(filepath)

def process_query(question, table, llm_type, query_engine_type):
    captured_output_str = "No trace available!"
    response = ""
    try:
        if SHOW_TRACE_ON_UI:
            captured_output = OutputCapture()
            sys.stdout = captured_output
        response = wrapper.process_query(question, table, 
            llm_type, query_engine_type)
        if SHOW_TRACE_ON_UI:
            sys.stdout = sys.__stdout__

        if SHOW_TRACE_ON_UI and captured_output is not None:
            captured_output_str = captured_output.get_output()
            
    except Exception as e:
        response = f"Error:\n{str(e)}"
        traceback.print_exc()
    return (response, captured_output_str)

st.sidebar.title("Inference Traces")
uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
if uploaded_file is not None:
    debug_info = st.sidebar.empty()
    table = process_cvs(uploaded_file)
    st.write("Table Preview")
    st.dataframe(table.head(5))

    llm_type = st.selectbox("LLM Type", [GPT_LLM, LOCAL_LLM])
    query_engine_type = st.selectbox("Query Engine", [TEXT2SQL_ENGINE, CHAINOFTABLE_ENGINE])
    question = st.text_input("Question", "")
    if question and st.button("Query"):
        (response, captured_output_str) = process_query(question, table, llm_type, query_engine_type)
        st.text_area("Response", response, height=2, max_chars=20)
        debug_info.text_area("", captured_output_str, height=600)
else:
    st.write("Awaiting CSV file to be uploaded.")
