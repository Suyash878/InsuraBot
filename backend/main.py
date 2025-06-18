from fastapi import FastAPI, Request, Query
from mindsdb import sheets_integration, kb_manager, semantic_query, jobs
import uvicorn

app = FastAPI(title="MindsDB Insurance Assistant")

@app.get("/")
def root():
    return {"msg": "Insurance Assistant API is live."}

@app.get("/knowledge-bases")
async def list_kbs():
    return kb_manager.list_knowledge_bases()

@app.get("/query")
async def query_kb(content_column: str = Query(None, description="Column to search content in")):
    return semantic_query.semantic_search(content_column)

@app.get("/query/agent")

@app.post("/register-sheet")
async def init_sheets(request: Request):
    body = await request.json()
    spreadsheet_id = body.get("spreadsheet_id")
    sheet_name = body.get("sheet_name")
    data_description = body.get("data_description", "general data")  # New field
    return sheets_integration.init_sheets_db(spreadsheet_id, sheet_name, data_description)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)