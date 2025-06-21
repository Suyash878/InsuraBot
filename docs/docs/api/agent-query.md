---
id: agent-query
title: Agent Query API
sidebar_label: Agent Query
---

# Agent Chat

The Agent Query API allows you to interact with AI agents and maintain conversation history through chat sessions.

## Overview

This endpoint enables you to send questions to specific agents and receive intelligent responses. The API automatically manages chat sessions and maintains conversation history for context-aware interactions.

---

## Query Agent

Send a question to an AI agent and receive an intelligent response with automatic chat session management.

### Endpoint

```http
POST /query/agent
```

### Request Body

The request body should contain a JSON object with the following properties:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_name` | `string` | ✅ | Name of the agent to query |
| `question` | `string` | ✅ | Question or message to send to the agent |
| `chat_id` | `string` | ❌ | Existing chat session ID (creates new if omitted) |

### Example Request

```json
{
  "agent_name": "customer_support",
  "question": "What are your business hours?",
  "chat_id": "chat_12345"
}
```

### Response

#### Success Response

**Status Code:** `200 OK`

```json
{
  "status": "success",
  "answer": "Our business hours are Monday to Friday, 9 AM to 6 PM EST. We're closed on weekends and major holidays.",
  "chat_id": "chat_12345",
  "timestamp": "2025-06-20T14:30:00Z"
}
```

#### Error Response

**Status Code:** `400 Bad Request`

```json
{
  "status": "error",
  "message": "Both agent_name and question are required"
}
```

**Status Code:** `404 Not Found`

```json
{
  "status": "error",
  "message": "Agent 'customer_support' not found"
}
```

### cURL Example

```bash
curl -X POST "http://127.0.0.1:8000/query/agent" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "customer_support",
    "question": "What are your business hours?",
    "chat_id": "chat_12345"
  }'
```

### Python Example

```python
import requests

url = "http://127.0.0.1:8000/query/agent"
payload = {
    "agent_name": "customer_support",
    "question": "What are your business hours?",
    "chat_id": "chat_12345"  # Optional
}

response = requests.post(url, json=payload)
data = response.json()

if data["status"] == "success":
    print(f"Agent: {data['answer']}")
    print(f"Chat ID: {data['chat_id']}")
else:
    print(f"Error: {data['message']}")
```

### JavaScript Example

```javascript
const response = await fetch('http://127.0.0.1:8000/query/agent', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    agent_name: 'customer_support',
    question: 'What are your business hours?',
    chat_id: 'chat_12345' // Optional
  })
});

const data = await response.json();

if (data.status === 'success') {
  console.log('Agent Response:', data.answer);
  console.log('Chat ID:', data.chat_id);
} else {
  console.error('Error:', data.message);
}
```

---

## Chat Session Management

### New Chat Session

If no `chat_id` is provided, the API automatically creates a new chat session:

```json
{
  "agent_name": "customer_support",
  "question": "Hello, I need help with my order"
}
```

Response includes the new `chat_id`:

```json
{
  "status": "success",
  "answer": "Hello! I'd be happy to help you with your order. Could you please provide your order number?",
  "chat_id": "chat_67890"
}
```

### Continuing Conversation

Use the returned `chat_id` to continue the conversation with context:

```json
{
  "agent_name": "customer_support",
  "question": "My order number is ORD-12345",
  "chat_id": "chat_67890"
}
```

---

## Error Codes

| Status | Message | Description |
|--------|---------|-------------|
| `error` | `Both agent_name and question are required` | Missing required parameters |
| `error` | `Agent '{name}' not found` | Specified agent does not exist |
| `error` | `Chat session not found` | Invalid chat_id provided |
| `error` | `Agent temporarily unavailable` | Agent is currently offline or busy |

---

## Notes

- Chat sessions maintain conversation context for better responses
- Messages are automatically stored in chat history
- Agent responses are generated based on the agent's knowledge base and training
- Chat sessions persist until explicitly deleted or expired
- The `chat_id` is required for follow-up questions in the same conversation