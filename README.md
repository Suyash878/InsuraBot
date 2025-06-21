<p align="center">
  <img src="https://github.com/user-attachments/assets/0c062d3c-a3a6-4840-bd82-97ebfb1e0c6e" width="400"/>
</p>
**SmartDB-API** is an intelligent assistant powered by MindsDB and fine-tuned domain LLMs.

Whether you're exploring large datasets, analyzing customer queries, or automating support — SmartAssist gives you **semantic search**, **AI classification**, **intelligent data analysis**, and **Google Sheets integration** all in one platform.

---

## Features

### Semantic Search on your Data
Search your documents and spreadsheets using natural language queries. SmartAssist uses MindsDB's Knowledge Bases to understand what you mean — not just exact keywords.

> _Example:_ "Show me all claims related to dental treatments in 2024"

---

### AI Agent Data Analysis
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

### Seamless Google Sheets Integration
Just provide a **Google Sheets ID and sheet name** — no need to upload files. SmartAssist connects it as a **live database** in MindsDB.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+ (for documentation)
- MindsDB account or local installation
- Google Sheets with public access or proper API credentials

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/SmartDB.git
   cd SmartDB
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your MindsDB credentials and configuration
   ```

4. **Install documentation dependencies:**
   ```bash
   cd docs
   npm install
   cd ..
   ```

### Running the Application

1. **Start the FastAPI backend:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Run the documentation site:**
   ```bash
   cd docs
   npm start
   ```
   The documentation will be available at `http://localhost:3000`

3. **Access the API:**
   - FastAPI backend: `http://localhost:8000`
   - Interactive API docs: `http://localhost:8000/docs`
   - ReDoc documentation: `http://localhost:8000/redoc`

---

## Documentation

### API Reference
Visit the **Docusaurus documentation site** at `http://localhost:3000` for comprehensive API documentation, including:

- **Getting Started Guide**: Step-by-step setup instructions
- **API Endpoints**: Detailed documentation for all available endpoints
- **Examples**: Code samples and use cases
- **Integration Guides**: How to connect with Google Sheets and other data sources
- **Troubleshooting**: Common issues and solutions

### Building Documentation for Production

```bash
cd docs
npm run build
npm run serve
```

---

## How It Works - Under the Hood with MindsDB

SmartAssist leverages MindsDB's powerful capabilities to provide intelligent data analysis and semantic search. Here's how the magic happens:

### 1. Data Connection & Integration

When you register a Google Sheet using the `/register-sheet` endpoint, the system:

```sql
-- Creates a live database connection in MindsDB
CREATE DATABASE your_sheet_db
WITH engine = 'sheets',
parameters = {
  "spreadsheet_id": "your_spreadsheet_id",
  "sheet_name": "your_sheet_name"
};
```

- **Live Connection**: Your Google Sheet becomes a queryable database in MindsDB
- **Real-time Sync**: Changes in your sheet are immediately available for analysis
- **No Data Migration**: No need to upload or duplicate your data

### 2. Knowledge Base Creation

SmartAssist automatically creates a MindsDB Knowledge Base for semantic search:

```sql
-- Creates an intelligent knowledge base
CREATE KNOWLEDGE_BASE your_sheet_kb
FROM your_sheet_db
WITH engine = 'chromadb',
embeddings_model = 'sentence-transformers/all-MiniLM-L6-v2';
```

**What happens:**
- **Vectorization**: Your data is converted into high-dimensional vectors that capture semantic meaning
- **Embeddings**: Each row and column is processed to understand context and relationships
- **Indexing**: Creates searchable indexes for fast retrieval based on meaning, not just keywords

### 3. AI Agent Creation

Each dataset gets its own specialized AI agent powered by MindsDB's ML capabilities:

```sql
-- Creates an intelligent agent for your data
CREATE AGENT your_sheet_agent
USING
  model = 'gpt-4',
  skills = ['knowledge_base'],
  knowledge_base = 'your_sheet_kb',
  database = 'your_sheet_db';
```

**Agent Capabilities:**
- **Data Structure Understanding**: Automatically analyzes your columns, data types, and relationships
- **Context Awareness**: Maintains conversation history for multi-turn analysis
- **SQL Generation**: Converts natural language questions into optimized SQL queries
- **Result Interpretation**: Provides human-readable insights from raw data

### 4. Query Processing Pipeline

When you ask a question, here's what happens:

1. **Natural Language Processing**: Your question is parsed and understood using LLMs
2. **Intent Recognition**: The system determines what type of analysis you need
3. **Query Generation**: Automatically generates appropriate SQL queries or knowledge base searches
4. **Data Retrieval**: Executes queries against your live data sources
5. **Result Processing**: Analyzes results and generates insights
6. **Response Generation**: Provides human-readable answers with context

### 5. Semantic Search Flow

For content-based searches:

```python
# Example: "Show me all claims related to dental treatments"
# 1. Query vectorization
query_vector = embed_text("dental treatments")

# 2. Similarity search in knowledge base
similar_content = knowledge_base.search(
    query_vector, 
    limit=10, 
    threshold=0.7
)

# 3. Context-aware response generation
response = agent.generate_response(
    query="Show me all claims related to dental treatments",
    context=similar_content
)
```

### 6. Chat History & Context Management

- **Session Management**: Each conversation maintains context across multiple queries
- **Memory**: Previous questions and answers inform future responses
- **Learning**: Agents improve their understanding of your specific data patterns over time

### 7. Real-time Data Analysis

MindsDB's architecture enables:
- **Live Queries**: Always working with the most current data
- **Automated Insights**: Background analysis identifies trends and anomalies
- **Predictive Capabilities**: Can forecast trends based on historical patterns
- **Multi-source Integration**: Combine data from multiple sheets or databases

---

## Configuration

### Environment Variables

```bash
# MindsDB Configuration
MINDSDB_URL=https://cloud.mindsdb.com
MINDSDB_USERNAME=your_username
MINDSDB_PASSWORD=your_password

# Google Sheets API (if using private sheets)
GOOGLE_SHEETS_CREDENTIALS_PATH=path/to/credentials.json

# Application Settings
DEBUG=true
LOG_LEVEL=info
```

### Advanced Configuration

For production deployments, you can configure:
- Custom embedding models
- Different vector databases
- Multiple LLM providers
- Custom agent personalities
- Data preprocessing pipelines

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

- **Documentation**: Visit `http://localhost:3000` for detailed guides
- **Issues**: Report bugs and request features on GitHub
- **Community**: Join our Discord for discussions and support

---

**Tip:**  
Start with the documentation site to explore all available features and see live examples of the API in action!
