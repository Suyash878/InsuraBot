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
CREATE AGENT orders_agent
USING
    model = 'gemini-2.0-flash',
    google_api_key = '{GEMINI_API_KEY}',
    include_knowledge_bases = ['mindsdb.orders_data_kb'],
    include_tables = ['orders_data.orders_data'],
    prompt_template = 'mindsdb.orders_data_kb stores orders of various customers. orders_data.orders_data stores orders of various customers.';
"""

try:
    result = con.query(query)
    print("Agent created successfully!")
    result.fetch()
except Exception as e:
    print(f"Error: {str(e)}")
