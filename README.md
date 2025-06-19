# NexusLore — Your AI Copilot for Your Data - (WIP)

SmartAssist is an intelligent assistant powered by MindsDB and fine-tuned domain LLMs.

Whether you're exploring large datasets, analyzing customer queries, or automating support — SmartAssist gives you **semantic search**, **AI classification**, **intelligent data analysis**, and **Google Sheets integration** all in one platform.

---

## Features

### 🔍 Semantic Search on your Data
Search your documents and spreadsheets using natural language queries. SmartAssist uses MindsDB's Knowledge Bases to understand what you mean — not just exact keywords.

> _Example:_ "Show me all claims related to dental treatments in 2024"

---

### 🤖 AI Agent Data Analysis
Interact with intelligent AI agents that automatically scan and analyze your data to provide relevant insights and answers. Each dataset gets its own specialized agent that understands your data structure and can answer complex questions about patterns, trends, and relationships in your data.

**Key Capabilities:**
- **Automatic Data Understanding**: Agents analyze your data structure, column relationships, and data types
- **Natural Language Queries**: Ask questions in plain English about your data
- **Contextual Responses**: Get answers that reference specific data points and provide actionable insights
- **Chat History**: Maintain conversation context across multiple queries for deep-dive analysis
- **Real-time Analysis**: Agents work with live data from your connected sources

> _Examples:_
> - "What are the top 3 product categories by sales this quarter?"
> - "Show me any unusual patterns in customer complaints from last month"
> - "Which regions have the highest customer satisfaction scores?"
> - "Are there any correlations between order size and customer retention?"

---

### 📊 Seamless Google Sheets Integration
Just provide a **Google Sheets ID and sheet name** — no need to upload files. SmartAssist connects it as a **live database** in MindsDB.

```sql
CREATE DATABASE insurance_data
WITH engine = 'sheets',
parameters = {
  "spreadsheet_id": "<YOUR_SPREADSHEET_ID>",
  "sheet_name": "<SHEET_NAME>"
};
```

## API Reference

Interact with MindsDB-powered knowledge bases, agents, and chat history via this FastAPI backend.

---

## Endpoints

### `GET /`
**Description:**  
Health check for the API.

**Response:**
```json
{"msg": "Data Assistant API is live."}
```

**Example:**
```bash
curl http://localhost:8000/
```

---

### `GET /knowledge-bases`
**Description:**  
List all available knowledge bases.

**Response:**
```json
{
  "status": "success",
  "knowledge_bases": [
    {
      "name": "sheet1_kb",
      "engine": "chromadb",
      "created_at": "2025-06-17 10:00:00"
    }
    // ... other knowledge bases
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/knowledge-bases
```

---

### `GET /query`
**Description:**  
Query the knowledge base.  
- If `content_column` is provided as a query parameter, performs a content-based search.
- If not provided, returns all data.

**Parameters:**
- `content_column` (optional, string): The content to search for.

**Response:**
```json
{
  "status": "success",
  "data": [ ... ],
  "search_type": "content_based" // or "full"
}
```

**Examples:**
```bash
# Content-based search
curl "http://localhost:8000/query?content_column=Office Supplies"

# Return all data
curl "http://localhost:8000/query"
```

---

### `POST /query/agent`
**Description:**  
Ask a question to an AI agent and store the Q&A in chat history.

**Request Body:**
```json
{
  "agent_name": "sales_data_agent",
  "question": "Show me total sales by region",
  "chat_id": "optional-chat-id"
}
```
- `agent_name` (string, required): Name of the agent to query.
- `question` (string, required): The question to ask.
- `chat_id` (string, optional): Existing chat session ID. If omitted, a new chat is created.

**Response:**
```json
{
  "status": "success",
  "agent": "sales_data_agent",
  "question": "Show me total sales by region",
  "answer": "...",
  "chat_id": "generated-or-provided-chat-id"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/query/agent \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "sales_data_agent", "question": "Show me total sales by region"}'
```

---

### `POST /register-sheet`
**Description:**  
Register a Google Sheet as a knowledge base and agent.

**Request Body:**
```json
{
  "spreadsheet_id": "your_spreadsheet_id",
  "sheet_name": "your_sheet_name",
  "data_description": "customer transaction records",
  "metadata_columns": ["sales_rep", "region"],
  "content_columns": ["product", "description"]
}
```
- `spreadsheet_id` (string, required): Google Spreadsheet ID.
- `sheet_name` (string, required): Name of the sheet.
- `data_description` (string, optional): Description of the data.
- `metadata_columns` (array of strings, optional): Metadata columns.
- `content_columns` (array of strings, optional): Content columns.

**Response:**
```json
{
  "status": "success",
  "message": "Initialized: Google Sheets DB, Knowledge Base 'your_sheet_name_kb', and Agent 'your_sheet_name_agent'"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/register-sheet \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
    "sheet_name": "orders",
    "data_description": "customer transaction records",
    "metadata_columns": ["sales_rep", "region"],
    "content_columns": ["product", "description"]
  }'
```

---

### `GET /chat/{chat_id}/history`
**Description:**  
Retrieve the chat history for a given chat session.

**Parameters:**
- `chat_id` (string, required): The chat session ID.

**Response:**
```json
{
  "status": "success",
  "chat_id": "your_chat_id",
  "history": [
    {
      "question": "Show me total sales by region",
      "answer": "...",
      "timestamp": "2025-06-20T12:34:56"
    }
    // ... more Q&A pairs
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/chat/your_chat_id/history
```

---

## API Documentation

- Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

**Tip:**  
Replace `localhost:8000` with your server's address if running remotely.

---