import mindsdb_sdk
from dotenv import load_dotenv
import os
from . import kb_manager 

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Using same key for Gemini

# Connect to local MindsDB instance
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

def init_sheets_db(
    id: str,
    spreadsheet_id: str,
    sheet_name: str,
    data_description: str,
    metadata_columns: list,
    content_columns: list
):
    try:
        # Create a dynamic database name
        db_name = f"{sheet_name}_db"

        # Create pgvector database first (separate query)
        pgvector_query = """
        CREATE DATABASE my_pgvector
        WITH ENGINE = 'pgvector',
        PARAMETERS = {
            "host": "172.17.0.1",
            "port": 5432,
            "database": "postgres",
            "user": "user",
            "password": "password",
            "distance": "cosine"
        };
        """
        
        try:
            con.query(pgvector_query).fetch()
        except Exception as pgv_error:
            # pgvector db might already exist, continue
            print(f"pgvector creation note: {pgv_error}")

        # Create sheets database (separate query with proper escaping)
        sheets_query = f"""
        CREATE DATABASE {db_name}
        WITH
            engine = 'sheets',
            parameters = {{
                "spreadsheet_id": "{spreadsheet_id}",
                "sheet_name": "{sheet_name}"
            }};
        """
        con.query(sheets_query).fetch()
        
        # Pass db_name to KB creation and other logic as needed
        kb_response = kb_manager.create_kb(sheet_name, metadata_columns, content_columns, db_name, id)
        if kb_response["status"] == "error":
            return kb_response
            
        # Insert data into knowledge base
        insert_response = kb_manager.insert_into_kb(sheet_name, db_name)
        if insert_response["status"] == "error":    
            return insert_response
            
        # Create AI agent (fixed f-string formatting)
        agent_query = f"""
        CREATE AGENT {sheet_name}_agent
        USING
            model = 'gemini-2.0-flash',
            google_api_key = '{GEMINI_API_KEY}',
            include_knowledge_bases = ['mindsdb.{sheet_name}_kb'],
            include_tables = ['{db_name}.{sheet_name}'],
            prompt_template = '
                mindsdb.{sheet_name}_kb stores {data_description}
                {db_name}.{sheet_name} stores {data_description}
                Use this data to answer questions accurately.
            ';
        """
        result = con.query(agent_query)
        print(result.fetch())
        return {
            "status": "success", 
            "message": f"Initialized: Google Sheets DB, Knowledge Base '{sheet_name}_kb', and Agent '{sheet_name}_agent'"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}