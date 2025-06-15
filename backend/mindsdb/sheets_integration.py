# backend/mindsdb/sheets_integration.py

import mindsdb_sdk
from mindsdb_sdk import connect
import uuid

mdb = connect('http://127.0.0.1:47334')

async def register_existing_sheet(spreadsheet_id: str, sheet_name: str) -> str:
    db_name = f"sheets_{uuid.uuid4().hex[:6]}"
    
    if not spreadsheet_id or not sheet_name:
        raise ValueError("Spreadsheet ID and Sheet Name must be provided")

    print(f"\nValues used in function:")
    print(f"spreadsheet_id: {spreadsheet_id}")
    print(f"sheet_name: {sheet_name}")

    mdb.databases.create(
        engine='sheets',
        name=db_name,
        connection_args={
            'spreadsheet_id': spreadsheet_id,
            'sheet_name': sheet_name
        }
    )

    return db_name
