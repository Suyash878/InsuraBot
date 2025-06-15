# backend/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mindsdb.sheets_integration import register_existing_sheet
import uvicorn

app = FastAPI()

class SheetInfo(BaseModel):
    spreadsheet_id: str
    sheet_name: str

@app.post("/register-sheet")
async def register_sheet(data: SheetInfo):
    try:
        db_name = await register_existing_sheet(data.spreadsheet_id, data.sheet_name)
        return {"message": f"Sheet registered in MindsDB as '{db_name}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "MindsDB Insurance Assistant is running 🚀"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
