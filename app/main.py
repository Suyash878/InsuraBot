from fastapi import FastAPI, Request, Query
from mindsdb import sheets_integration, kb_manager, semantic_query, agent, jobs_manager
from db.chat_history import ChatHistory
import uvicorn
job_manager = jobs_manager.JobManager()

app = FastAPI(title="MindsDB Insurance Assistant")
chat_db = ChatHistory()

@app.get("/")
def root():
    return {"msg": "Insurance Assistant API is live."}

@app.get("/knowledge-bases")
async def list_kbs():
    return kb_manager.list_knowledge_bases()

@app.get("/query")
async def query_kb(
    kb_name: str = Query(..., description="Knowledge base name to query from"),
    content_column: str = Query(None, description="Column to search content in")
):
    return semantic_query.semantic_search(kb_name, content_column)

@app.get("/chat/{chat_id}/history")
async def get_chat_history(chat_id: str):
    try:
        history = chat_db.get_chat_history(chat_id)
        return {
            "status": "success",
            "chat_id": chat_id,
            "history": [
                {
                    "question": msg[0],
                    "answer": msg[1],
                    "timestamp": msg[2]
                } for msg in history
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/query/agent")
async def agent_query(request: Request):
    body = await request.json()
    agent_name = body.get("agent_name")
    question = body.get("question")
    chat_id = body.get("chat_id")
    
    if not agent_name or not question:
        return {
            "status": "error",
            "message": "Both agent_name and question are required"
        }
    
    # Create new chat if no chat_id provided
    if not chat_id:
        chat_id = chat_db.create_chat(agent_name)
    
    # Query agent
    response = agent.query_agent(agent_name, question)
    
    if response["status"] == "success":
        # Store message in chat history
        chat_db.add_message(chat_id, question, response["answer"])
        response["chat_id"] = chat_id
    
    return response

@app.post("/register-sheet", tags=["Knowledge Base"])
async def init_sheets(request: Request):
    body = await request.json()
    id = body.get("id")  
    spreadsheet_id = body.get("spreadsheet_id")
    sheet_name = body.get("sheet_name")
    data_description = body.get("data_description", "general data")
    metadata_columns = body.get("metadata_columns", [])
    content_columns = body.get("content_columns", [])
    return sheets_integration.init_sheets_db(
        id, 
        spreadsheet_id,
        sheet_name,
        data_description,
        metadata_columns,
        content_columns
    )

@app.post("/jobs/create", tags=["Jobs"])
async def create_job(payload: jobs_manager.CreateJobRequest):
    return job_manager.create_job(payload)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)