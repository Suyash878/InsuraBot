import mindsdb_sdk
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMBEDDING_API_KEY = os.getenv('EMBEDDING_API_KEY')
RERANKING_API_KEY = os.getenv('RERANKING_API_KEY')

con = mindsdb_sdk.connect()
con = mindsdb_sdk.connect('http://127.0.0.1:47334')

databases = con.databases.list()

database = databases[0]

query = con.query(f"""
CREATE KNOWLEDGE_BASE random_case_kb
USING
    embedding_model = {{
        "provider": "gemini",
        "model_name" : "text-embedding-004",
        "api_key": "{EMBEDDING_API_KEY}"
    }},
    reranking_model = {{
        "provider": "together_ai",
        "model_name": "Salesforce/Llama-Rank-V1",
        "api_key": "{RERANKING_API_KEY}"
    }},
    metadata_columns = ['sales_rep'],
    content_columns = ['region'],
    id_column = 'transaction_id';""")

print(query.fetch())