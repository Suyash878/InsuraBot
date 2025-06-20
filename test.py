import mindsdb_sdk
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Connect to MindsDB
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

# Create agent query with proper string formatting
query = f"""
SELECT *
FROM orders_data_kb_chromadb.default_collection
LIMIT 50;
"""

try:
    result = con.query(query)
    print("Agent created successfully!")
    result.fetch()
except Exception as e:
    print(f"Error: {str(e)}")
