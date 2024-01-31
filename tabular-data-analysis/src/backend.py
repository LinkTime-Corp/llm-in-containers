import llama_index
import json, os, time
from chain_of_table_pack.base import ChainOfTableQueryEngine, serialize_table
from constants import TEXT2SQL_ENGINE, CHAINOFTABLE_ENGINE, GPT_LLM, LOCAL_LLM
from llama_index import ServiceContext
from llama_index import set_global_service_context
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import OpenAILike, OpenAI
from mix_self_consistency_pack.base import MixSelfConsistencyQueryEngine

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
    for model in config["models"]:
        if CPU_ONLY:
            if model["type"] == "CPU_Only":
                MODEL_NAME = model["name"]
        else:
            if model["type"] == "GPU_Enabled":
                MODEL_NAME = model["name"]

MAC_M1_LUNADEMO_CONSERVATIVE_TIMEOUT = 10 * 60  # sec

class QueryEngineWrapper:
    local_llm = None
    openai_llm = None
    def __init__(self):
        self.openai_llm = OpenAI(model=OPENAI_API_MODEL)
        self.local_llm = OpenAILike(
            api_base=API_BASE,
            api_key=API_KEY,
            model=MODEL_NAME,
            is_chat_model=True,
            is_function_calling_model=True,
            context_window=3900,
            timeout=MAC_M1_LUNADEMO_CONSERVATIVE_TIMEOUT,
        )

    def get_query_engine(self, table, llm_type, query_engine_type): 
        query_engine = None
        chosen_llm = None
        if llm_type == GPT_LLM:
            chosen_llm = self.openai_llm
            embed_model = OpenAIEmbedding(embed_batch_size=10)
            service_context = ServiceContext.from_defaults(
                chunk_size=1024, llm=chosen_llm, embed_model=embed_model)
        else:
            chosen_llm = self.local_llm
            service_context = ServiceContext.from_defaults(
                chunk_size=1024, llm=chosen_llm, embed_model="local")
            set_global_service_context(service_context)        

        text_paths = 3
        symbolic_paths = 3
        if CPU_ONLY and llm_type == LOCAL_LLM:
            text_paths = 1
            symbolic_paths = 1

        if query_engine_type == TEXT2SQL_ENGINE:
            query_engine = MixSelfConsistencyQueryEngine(
                            df=table, 
                            llm=chosen_llm, 
                            text_paths=text_paths, 
                            symbolic_paths=symbolic_paths, 
                            aggregation_mode="self-consistency", 
                            verbose=True)
        elif query_engine_type == CHAINOFTABLE_ENGINE:
            query_engine = ChainOfTableQueryEngine(
                            table=table, llm=chosen_llm, verbose=True)
        else:
            raise Exception("Invalid query engine type")
        return query_engine

    def process_query(self, question, table, llm_type, query_engine_type):
        query_engine = self.get_query_engine(table, llm_type, query_engine_type)
    
        start_time = time.time()  # Start time recording
        response = query_engine.query(question)
        end_time = time.time()  # End time recording
        time_spent = end_time - start_time  # Calculate duration
        # add time spent to the end of the response
        final_response = response.__str__() + "\nTime spent: {:.2f} seconds".format(time_spent)
        return final_response
