# NexusLore — Your AI Copilot for Your Data - (WIP)

SmartAssist is an intelligent assistant powered by MindsDB and fine-tuned domain LLMs.

Whether you're exploring large datasets, analyzing customer queries, or automating support — SmartAssist gives you **semantic search**, **AI classification**, and **Google Sheets integration** all in one platform.

---

## ✨ Features

### 🔍 Semantic Search on your Data
Search your documents and spreadsheets using natural language queries. SmartAssist uses MindsDB's Knowledge Bases to understand what you mean — not just exact keywords.

> _Example:_ “Show me all claims related to dental treatments in 2024”

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
