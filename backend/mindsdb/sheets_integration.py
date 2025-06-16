import mindsdb_sdk
from dotenv import load_dotenv
import os
from . import kb_manager

# Load environment variables
load_dotenv()

# Connect to local MindsDB instance
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

def init_sheets_db(spreadsheet_id: str, sheet_name: str):
    try:
        # Create sheets database
        sheets_query = f"""
        CREATE DATABASE sheets_datasource
        WITH
            engine = 'sheets',
            parameters = {{
                "spreadsheet_id": "{spreadsheet_id}",
                "sheet_name": "{sheet_name}"
            }};
        """
        con.query(sheets_query).fetch()
        
        # Create knowledge base with sheet name
        kb_response = kb_manager.create_kb(sheet_name)
        
        if kb_response["status"] == "error":
            return kb_response
            
        return {"status": "success", "message": f"Google Sheets DB and Knowledge Base '{sheet_name}_kb' initialized."}
    except Exception as e:
        return {"status": "error", "message": str(e)}