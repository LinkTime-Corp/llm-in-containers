from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Iterable, List, Optional, Sequence
import ast, json, os
import pandas as pd
from decimal import Decimal

script_dir = os.path.dirname(os.path.realpath(__file__))
upper_dir = os.path.dirname(script_dir)
config_path = os.path.join(f"{upper_dir}/conf", "config.json")
with open(config_path) as f:
    config = json.load(f)
    database_settings = config["database"]
    USER_NAME = database_settings["user"]
    PASSWORD = database_settings["password"]
    HOST = database_settings["host"]
    PORT = database_settings["port"]
    DB = database_settings["db"]

class DBEngine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
        
    db: SQLDatabase = Field(..., description="engine to use.")
    def __init__(self, **kwargs: Any,):
        db_url = f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DB}"
        db = SQLDatabase(create_engine(db_url), max_string_length=1000)
        super().__init__(db=db, **kwargs)

    def get_db(self) -> SQLDatabase:
        return self.db

    def get_dialect(self) -> str:
        try:
            return self.db.dialect
        except Exception as e:
            raise e

    def get_table_names(self) -> Iterable[str]:
        try:
            return self.db.get_usable_table_names()
        except Exception as e:
            raise e

    def get_table_sample(self, table_name: str, limit: int = 3) -> pd.DataFrame:
        try:
            samples = self.exec_db("select * from " + table_name + " limit " + str(limit))
            return pd.DataFrame(samples)
        except Exception as e:
            raise e

    def get_table_schema(self, table_name: str)-> str:
        try:
            schema_str = self.query_db("show create table " +table_name)
            schema = ast.literal_eval(schema_str)
            return schema[0][1]
        except Exception as e:
            raise e

    def query_db(self, query: str) -> str:
        try:
            return self.db.run(query)
        except Exception as e:
            raise e

    def exec_db(self, query: str) -> Sequence[Dict[str, Any]]:
        try:
            return self.db._execute(query)
        except Exception as e:
            raise e

if __name__ == "__main__":
    db_engine = DBEngine()
    print(db_engine.get_dialect())
    print("------------------")
    tables = db_engine.get_table_names()
    print(tables[0])
    print("------------------")
    print(db_engine.get_table_schema(tables[0]))
    print("------------------")
    print(db_engine.get_table_sample(tables[0]))
    print("------------------")

