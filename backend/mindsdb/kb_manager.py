import mindsdb_sdk
from dotenv import load_dotenv
import os
import json
import pandas as pd

load_dotenv()

EMBEDDING_API_KEY = os.getenv('EMBEDDING_API_KEY')
RERANKING_API_KEY = os.getenv('RERANKING_API_KEY')

# Connecting to MindsDB
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

def list_knowledge_bases():
    try:
        query = """
        SHOW KNOWLEDGE BASES;
        """
        result = con.query(query)
        
        # Convert to pandas DataFrame and then to dict
        df = pd.DataFrame(result.fetch())
        
        # Convert DataFrame to a list of dictionaries
        kbs = df.to_dict('records')
        
        # Ensure all numpy types are converted to Python native types
        kbs = json.loads(json.dumps(kbs, default=str))
        
        return {"status": "success", "knowledge_bases": kbs}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_kb(kb_name: str, metadata_columns: list, content_columns: list, db_name: str, id: str):
    try:
        query = f"""
        CREATE KNOWLEDGE_BASE {kb_name}_kb
        USING
            embedding_model = {{
                "provider": "gemini",
                "model_name": "text-embedding-004",
                "api_key": "{EMBEDDING_API_KEY}"
            }},
            reranking_model = {{
                "provider": "together_ai",
                "model_name": "Salesforce/Llama-Rank-V1",
                "api_key": "{RERANKING_API_KEY}"
            }},
            metadata_columns = {metadata_columns},
            content_columns = {content_columns},
            id_column = {id};
        """
        con.query(query).fetch()
        return {"status": "success", "message": f"Knowledge base {kb_name}_kb created in database {db_name}."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def insert_into_kb(kb_name: str, db_name: str):
    try:
        query = f"""
        INSERT INTO {kb_name}_kb
        SELECT * FROM {db_name}.{kb_name};
        """
        result = con.query(query)
        print(result.fetch())
        return {"status": "success", "message": f"Data inserted into {kb_name}_kb."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# NOT USING THIS BECAUSE USING CHROMA DB--------------------
# def create_kb_index(kb_name: str):
#     try:
#         query = f"""
#         CREATE INDEX ON KNOWLEDGE_BASE {kb_name}_kb;
#         """
#         result = con.query(query)
#         print(result.fetch())
#         return {"status": "success", "message": f"Index created on {kb_name}_kb."}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
