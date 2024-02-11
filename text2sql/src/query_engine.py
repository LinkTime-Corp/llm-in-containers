from constants import LOCAL_LLM, GPT_LLM
from db_engine import DBEngine
from langchain.chains import create_sql_query_chain
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os, json, re, yaml, time

script_dir = os.path.dirname(os.path.realpath(__file__))
upper_dir = os.path.dirname(script_dir)
config_path = os.path.join(f"{upper_dir}/conf", "config.json")
with open(config_path) as f:
    config = json.load(f)
    API_BASE = config["API_BASE"]
    API_KEY = config["API_KEY"]
    CPU_ONLY = config["CPU_Only"]
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
    OPENAI_API_MODEL = config["OPENAI_API_MODEL"]
    model_list = config["models"]
    for model in model_list:
        if CPU_ONLY and model["type"] == "CPU_Only":
            LOCAL_MODEL_NAME = model["name"]
        if not CPU_ONLY and model["type"] == "GPU_Enabled":
            LOCAL_MODEL_NAME = model["name"]

class SQLEngineWrapper:
    gpt_agent = None
    local_chain = None
    db_engine = None
    def __init__(self):
        self.db_engine = DBEngine()
        db = self.db_engine.get_db()
        self.local_chain = self.init_local_chain(db)
        self.gpt_agent = self.init_openai_agent(db)

    def init_openai_agent(self, db):
        openai_llm = ChatOpenAI(model_name=OPENAI_API_MODEL)
        return create_sql_agent(openai_llm, db=db,
            agent_type="openai-tools", verbose=True)

    def init_local_chain(self, db):
        local_llm = ChatOpenAI(model_name=LOCAL_MODEL_NAME, openai_api_base=API_BASE)
        write_query = create_sql_query_chain(local_llm, db)
        return write_query

    def process_query(self, question, llm_type):
        start_time = time.time()  # Start time recording
        response = None
        if llm_type == GPT_LLM:
            response_dict = self.gpt_agent.invoke(question)
            # convert the response_dict into a string
            response = ""
            for key, value in response_dict.items():
                response = response + key + ": " + value + "  \n"
        else:
            text = self.local_chain.invoke({"question": question})
            sql_text = self.extract_sql_statements(text)
            response = self.db_engine.query_db(sql_text)

        end_time = time.time()  # End time recording
        time_spent = end_time - start_time  # Calculate duration
        final_response = response + "  \nTime spent: {:.2f} seconds".format(time_spent)
        return final_response

    def extract_sql_statements(self, text):
        # Regular expression to find substrings that could be SQL statements.
        # This pattern assumes SQL statements end with a semicolon and attempts to exclude common comment patterns.
        pattern = r"(?<![/\*])(?:.*?;)"
        
        # Using re.findall to extract all occurrences that match the pattern
        sql_statements = re.findall(pattern, text, flags=re.DOTALL)
        
        # Filtering out empty strings or strings that only contain whitespace
        sql_statements = [stmt.strip() for stmt in sql_statements if stmt.strip()]
        sql_text = ""
        for statement in sql_statements:
            sql_text += statement + "\n"
        return sql_text

if __name__ == "__main__":
    sql_agent = SQLEngineWrapper()
    question = "where is address of the office in San Francisco?"
    response = sql_agent.process_query(question, LOCAL_LLM)
    print(response)
