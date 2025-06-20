---
id: query
title: Query Data
sidebar_label: Query
---

# Query a Knowledge Base

Perform semantic search queries on your registered knowledge bases to find relevant information.

## Overview

The Query endpoint enables you to search through your knowledge bases using semantic similarity. This powerful feature allows you to find relevant information even when exact keyword matches aren't available, making it perfect for discovering insights and patterns in your data.

:::info
This endpoint uses semantic search powered by vector embeddings, which means it can find conceptually similar content even if the exact words don't match your query.
:::

## Endpoint

```http
GET /query
```

## Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `kb_name` | `string` | ✅ **Required** | Knowledge base name to search within |
| `content_column` | `string` | ❌ Optional | Specific column to search content in |

### Parameter Details

- **`kb_name`**: Must match an existing knowledge base name (use `/knowledge-bases` to see available options)
- **`content_column`**: When specified, searches only within that column; when omitted, searches across all content

## Example Requests

### Basic Knowledge Base Search

```http
GET /query?kb_name=sales_data_kb
```

### Column-Specific Search

```http
GET /query?kb_name=customer_feedback_kb&content_column=feedback_text
```

### URL Encoded Example

```http
GET /query?kb_name=product_inventory_kb&content_column=product%20description
```

## Response

### Success Response

```json
{
  "status": "success",
  "data": [
    {
      "id": "row_123",
      "content": "Premium wireless headphones with noise cancellation",
      "similarity_score": 0.92,
      "source_column": "product_description",
      "metadata": {
        "category": "Electronics",
        "price": "$299.99",
        "brand": "TechCorp"
      }
    },
    {
      "id": "row_456", 
      "content": "High-quality Bluetooth earbuds for active lifestyle",
      "similarity_score": 0.87,
      "source_column": "product_description",
      "metadata": {
        "category": "Electronics",
        "price": "$149.99",
        "brand": "SportTech"
      }
    }
  ],
  "search_type": "content_based",
  "total_results": 15,
  "kb_name": "product_inventory_kb"
}
```

### Full Search Response

```json
{
  "status": "success",
  "data": [
    {
      "id": "row_789",
      "content": "Customer reported excellent sound quality and comfort",
      "similarity_score": 0.94,
      "source_column": "feedback_text",
      "metadata": {
        "customer_id": "CUST_001",
        "rating": 5,
        "product": "Wireless Headphones"
      }
    }
  ],
  "search_type": "full",
  "total_results": 8,
  "kb_name": "customer_feedback_kb"
}
```

### Error Response

```json
{
  "status": "error",
  "message": "Knowledge base 'invalid_kb' not found"
}
```

## Response Fields

### Success Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always "success" for successful requests |
| `data` | `array` | Array of search result objects |
| `search_type` | `string` | Either "content_based" or "full" depending on search scope |
| `total_results` | `number` | Total number of results found |
| `kb_name` | `string` | The knowledge base that was searched |

### Search Result Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique identifier for the result row |
| `content` | `string` | The matching content text |
| `similarity_score` | `number` | Relevance score (0.0 to 1.0, higher is more relevant) |
| `source_column` | `string` | Which column the content came from |
| `metadata` | `object` | Additional data from other columns in the same row |

## Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `"Knowledge base 'name' not found"` | Invalid kb_name parameter | Check available knowledge bases with `/knowledge-bases` |
| `"Column 'name' not found in knowledge base"` | Invalid content_column parameter | Verify column names in your registered sheet |
| `"No content found for search"` | Empty knowledge base or no matching content | Ensure your knowledge base has data |
| `"Search query too short"` | Query parameters insufficient | Provide more specific search criteria |

## Search Types

### Content-Based Search (`content_column` specified)
- Searches within a specific column
- More focused and targeted results
- Better for finding specific types of information
- Returns `"search_type": "content_based"`

### Full Search (no `content_column`)
- Searches across all content columns
- Broader result set
- Good for general exploration
- Returns `"search_type": "full"`

## Use Cases

### 🔍 **Product Discovery**
```http
GET /query?kb_name=product_catalog_kb&content_column=description
```
Find products based on features or characteristics.

### 💬 **Customer Feedback Analysis**
```http
GET /query?kb_name=feedback_kb&content_column=comments
```
Discover patterns in customer feedback and reviews.

### 📊 **Data Exploration**
```http
GET /query?kb_name=sales_data_kb
```
Explore your data without knowing exact column names.

### 🎯 **Targeted Research**
```http
GET /query?kb_name=research_kb&content_column=findings
```
Search specific content types within your knowledge base.

## Integration Examples

### Basic Search Implementation

```javascript
// Search a knowledge base
async function searchKnowledgeBase(kbName, contentColumn = null) {
  try {
    let url = `/query?kb_name=${encodeURIComponent(kbName)}`;
    if (contentColumn) {
      url += `&content_column=${encodeURIComponent(contentColumn)}`;
    }
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.status === 'success') {
      console.log(`Found ${data.total_results} results in ${data.kb_name}`);
      return data.data;
    } else {
      console.error('Search failed:', data.message);
      return [];
    }
  } catch (error) {
    console.error('Search error:', error);
    return [];
  }
}
```

### Filter by Similarity Score

```javascript
// Get only high-relevance results
function getHighRelevanceResults(searchResults, threshold = 0.8) {
  return searchResults.filter(result => result.similarity_score >= threshold);
}
```

### Build Search Interface

```javascript
// Create a search form
function createSearchInterface() {
  const form = document.createElement('form');
  form.innerHTML = `
    <select id="kb-select" required>
      <option value="">Select Knowledge Base</option>
    </select>
    <input type="text" id="content-column" placeholder="Column name (optional)">
    <button type="submit">Search</button>
  `;
  
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const kbName = document.getElementById('kb-select').value;
    const contentColumn = document.getElementById('content-column').value || null;
    
    const results = await searchKnowledgeBase(kbName, contentColumn);
    displayResults(results);
  });
  
  return form;
}
```

## Best Practices

### Query Optimization

**✅ Good Practices:**
- Use specific knowledge base names
- Specify content_column for targeted searches
- URL encode parameters properly
- Handle empty result sets gracefully

**❌ Avoid:**
- Searching non-existent knowledge bases
- Very generic queries without context
- Ignoring similarity scores
- Not handling error responses

### Result Processing

- **Filter by Relevance**: Use similarity_score to filter results
- **Combine Metadata**: Use metadata fields for additional context
- **Paginate Results**: Handle large result sets appropriately
- **Cache Results**: Store frequently accessed search results

### Performance Tips

- **Targeted Searches**: Use content_column when you know what you're looking for
- **Batch Operations**: Group multiple searches when possible
- **Result Limits**: Consider implementing client-side result limiting
- **Async Processing**: Use asynchronous patterns for better UX

## Similarity Scores

Understanding similarity scores helps you filter and rank results:

| Score Range | Interpretation | Use Case |
|-------------|----------------|----------|
| `0.9 - 1.0` | Highly relevant | Exact or near-exact matches |
| `0.7 - 0.9` | Very relevant | Strong conceptual similarity |
| `0.5 - 0.7` | Moderately relevant | Related but not exact |
| `0.3 - 0.5` | Somewhat relevant | Weak connection |
| `0.0 - 0.3` | Low relevance | May not be useful |

## Related Endpoints

This endpoint works well with:

1. **`/knowledge-bases`**: Get available knowledge bases to search
2. **`/query/agent`**: Use search results to inform agent questions
3. **`/register-sheet`**: Add new data sources to search

## Next Steps

After getting search results:

1. **Analyze Patterns**: Look for trends in the returned data
2. **Ask Agent Questions**: Use insights to query your AI agents
3. **Refine Searches**: Adjust parameters based on result quality
4. **Export Results**: Save important findings for further analysis