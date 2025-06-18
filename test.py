import mindsdb_sdk
from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_API_KEY = os.getenv('EMBEDDING_API_KEY')
RERANKING_API_KEY = os.getenv('RERANKING_API_KEY')

# Connect to MindsDB
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

query = """
        SELECT *
FROM sheets_datasource.sales_data
LIMIT 50;"""

result = con.query(query)
print(result.fetch())