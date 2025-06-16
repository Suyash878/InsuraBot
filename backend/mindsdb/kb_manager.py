import mindsdb_sdk
from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_API_KEY = os.getenv('EMBEDDING_API_KEY')
RERANKING_API_KEY = os.getenv('RERANKING_API_KEY')

# Connecting to MindsDB
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

def create_kb(kb_name: str):
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
            metadata_columns = ['Customer_Name'],
            content_columns = ['Policy_Type'],
            id_column = 'Policy_ID';
        """
        result = con.query(query)
        print(result.fetch())
        return {"status": "success", "message": f"Knowledge base {kb_name}_kb created."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def insert_into_kb(kb_name: str):
    try:
        query = f"""
        INSERT INTO {kb_name}_kb
        SELECT * FROM sheets_datasource.{kb_name};
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
