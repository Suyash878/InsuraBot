from fastapi import FastAPI, Request
from mindsdb import sheets_integration, kb_manager, semantic_query, jobs, ai_tables
import uvicorn

app = FastAPI(title="MindsDB Insurance Assistant")

@app.get("/")
def root():
    return {"msg": "Insurance Assistant API is live."}

@app.post("/init-sheets-db")
async def init_sheets(request: Request):
    body = await request.json()
    spreadsheet_id = body.get("spreadsheet_id")
    sheet_name = body.get("sheet_name")
    return sheets_integration.init_sheets_db(spreadsheet_id, sheet_name)

@app.post("/query/")
async def query_kb(request: Request):
    body = await request.json()
    content_column = body.get("content_column", "Policy_type")
    return semantic_query.semantic_search(content_column)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)