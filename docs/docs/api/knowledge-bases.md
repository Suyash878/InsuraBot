---
id: knowledge-bases
title: Knowledge Bases
sidebar_label: Knowledge Bases
---

# List Knowledge Bases

Retrieve all available knowledge bases in your system.

## Overview

The Knowledge Bases endpoint provides a comprehensive list of all registered knowledge bases, including their metadata and creation details. This is essential for understanding what data sources are available for querying and analysis.

:::info
Knowledge bases are automatically created when you register Google Sheets or other data sources. Each knowledge base represents a searchable, indexed version of your data.
:::

## Endpoint

```http
GET /knowledge-bases
```

## Request

This endpoint requires no parameters or request body.

```http
GET /knowledge-bases
```

## Response

### Success Response

```json
{
  "status": "success",
  "knowledge_bases": [
    {
      "name": "sales_data_kb",
      "engine": "chromadb",
      "created_at": "2025-06-17 10:00:00"
    },
    {
      "name": "customer_feedback_kb",
      "engine": "chromadb", 
      "created_at": "2025-06-18 14:30:00"
    },
    {
      "name": "product_inventory_kb",
      "engine": "chromadb",
      "created_at": "2025-06-19 09:15:00"
    }
  ]
}
```

### Error Response

```json
{
  "status": "error",
  "message": "Unable to retrieve knowledge bases"
}
```

## Response Fields

### Success Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always "success" for successful requests |
| `knowledge_bases` | `array` | Array of knowledge base objects |

### Knowledge Base Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Unique identifier for the knowledge base |
| `engine` | `string` | Vector database engine used (typically "chromadb") |
| `created_at` | `string` | When the knowledge base was created (YYYY-MM-DD HH:MM:SS format) |

## Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `"Unable to retrieve knowledge bases"` | System or database issue | Try again later or contact support |
| `"Database connection error"` | Connection problem | Check system status or try again |
| `"Access denied"` | Insufficient permissions | Verify your account permissions |

## Use Cases

### 📊 **System Overview**
```http
GET /knowledge-bases
```
Get a complete overview of all available data sources for analysis.

### 🔍 **Data Source Discovery**
Before querying agents, check what knowledge bases are available for different topics.

### 📈 **Usage Monitoring**
Track when knowledge bases were created to understand data ingestion patterns.

### 🎯 **Integration Planning**
Identify existing knowledge bases before registering new ones to avoid duplicates.

## Knowledge Base Naming Conventions

Knowledge bases are typically named based on:

- **Source Data**: `sales_data_kb`, `customer_orders_kb`
- **Department**: `hr_policies_kb`, `marketing_campaigns_kb`  
- **Time Period**: `q1_2024_sales_kb`, `annual_reports_kb`
- **Data Type**: `feedback_kb`, `inventory_kb`, `transactions_kb`

## Integration Examples

### Check Available Knowledge Bases

```javascript
// Fetch all knowledge bases
async function getKnowledgeBases() {
  try {
    const response = await fetch('/knowledge-bases');
    const data = await response.json();
    
    if (data.status === 'success') {
      console.log('Available knowledge bases:');
      data.knowledge_bases.forEach(kb => {
        console.log(`- ${kb.name} (created: ${kb.created_at})`);
      });
      return data.knowledge_bases;
    } else {
      console.error('Failed to fetch knowledge bases:', data.message);
      return [];
    }
  } catch (error) {
    console.error('Error fetching knowledge bases:', error);
    return [];
  }
}
```

### Filter by Creation Date

```javascript
// Get recently created knowledge bases
function getRecentKnowledgeBases(knowledgeBases, days = 7) {
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - days);
  
  return knowledgeBases.filter(kb => {
    const createdDate = new Date(kb.created_at);
    return createdDate >= cutoffDate;
  });
}
```

### Build Knowledge Base Selector

```javascript
// Create dropdown options for knowledge base selection
function createKBSelector(knowledgeBases) {
  const selector = document.getElementById('kb-selector');
  
  knowledgeBases.forEach(kb => {
    const option = document.createElement('option');
    option.value = kb.name;
    option.textContent = `${kb.name} (${kb.created_at})`;
    selector.appendChild(option);
  });
}
```

## Knowledge Base Lifecycle

### 1. **Creation**
Knowledge bases are created when you register data sources:
```json
POST /register-sheet
{
  "id": "sales-data-2024",
  "spreadsheet_id": "...",
  "sheet_name": "Sales"
}
```

### 2. **Indexing**
Data is processed and indexed using ChromaDB for semantic search.

### 3. **Querying**
Knowledge bases become available for agent queries and semantic search.

### 4. **Updates**
Re-registering with the same ID updates the knowledge base content.

## Best Practices

### Regular Monitoring
- **Check Regularly**: Monitor available knowledge bases to understand your data landscape
- **Track Creation Dates**: Identify when new data sources were added
- **Verify Completeness**: Ensure all expected knowledge bases are present

### Naming Strategy
- **Use Descriptive Names**: Make knowledge base purposes clear
- **Include Dates**: Add time periods for time-sensitive data
- **Consistent Conventions**: Follow team naming standards

### Integration Patterns
- **Cache Results**: Store knowledge base list to avoid repeated API calls
- **Dynamic UI**: Build interfaces that adapt to available knowledge bases
- **Error Handling**: Gracefully handle cases where knowledge bases are unavailable

## Related Endpoints

After getting your knowledge bases list, you can:

1. **Query Specific Knowledge Bases**: Use the semantic search endpoint
2. **Create AI Agents**: Reference knowledge bases when setting up agents
3. **Register New Data**: Add more knowledge bases via sheet registration

## System Information

:::tip
**Vector Engine**: All knowledge bases use ChromaDB for high-performance semantic search and similarity matching.

**Automatic Updates**: Knowledge bases are automatically updated when you re-register data sources with the same ID.
:::

## Next Steps

Once you have your knowledge bases list:

1. **Semantic Search**: Query specific knowledge bases for relevant information
2. **Agent Creation**: Use knowledge bases to power your AI agents
3. **Data Analysis**: Understand what data is available for analysis
4. **System Maintenance**: Monitor and manage your knowledge base collection