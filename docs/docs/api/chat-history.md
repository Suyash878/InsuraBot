---
id: chat-history
title: Chat Management
sidebar_label: Chat Management
---

# Chat Management

Manage and retrieve chat sessions and conversation history with AI agents.

## Overview

The Chat Management endpoints allow you to list all chat sessions and access conversation history for specific chats. This is useful for reviewing past conversations, continuing discussions, or analyzing interaction patterns with your AI agents.

:::info
Chat history is automatically maintained when you use the Agent Q&A endpoint. Each chat session preserves the full conversation context.
:::

---

## List All Chats

Get a list of all chat sessions with their basic information.

### Endpoint

```http
GET /chats
```

### Parameters

This endpoint requires no parameters.

### Example Request

```http
GET /chats
```

### Response

#### Success Response

```json
{
  "status": "success",
  "chats": [
    {
      "chat_id": "auto_generated_chat_123",
      "agent_name": "sales_data_agent",
      "created_at": "2025-06-20T09:15:30"
    },
    {
      "chat_id": "auto_generated_chat_456",
      "agent_name": "customer_support_agent",
      "created_at": "2025-06-19T14:22:15"
    },
    {
      "chat_id": "manual_chat_789",
      "agent_name": "inventory_agent",
      "created_at": "2025-06-18T11:30:45"
    }
  ]
}
```

#### Error Response

```json
{
  "status": "error",
  "message": "Failed to retrieve chat list"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | "success" or "error" |
| `chats` | `array` | Array of chat session objects |

#### Chat Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `chat_id` | `string` | Unique identifier for the chat session |
| `agent_name` | `string` | Name of the agent used in this chat |
| `created_at` | `string` | When the chat was created (ISO 8601 format) |

### Use Cases

- **📋 Session Overview**: Get a quick overview of all your chat sessions
- **🔍 Find Specific Chats**: Locate chat sessions by agent or creation date
- **🗂️ Chat Organization**: Manage and organize your conversations
- **📊 Usage Analytics**: Analyze which agents are used most frequently

---

## Get Chat History

Retrieve the complete conversation history for a specific chat session.

### Endpoint

```http
GET /chat/{chat_id}/history
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chat_id` | `string` | ✅ **Required** | The unique chat session identifier |

#### Parameter Details

- **`chat_id`**: The unique identifier from the chat list or returned when you first query an agent

### Example Request

```http
GET /chat/auto_generated_chat_123/history
```

### Response

#### Success Response

```json
{
  "status": "success",
  "chat_id": "auto_generated_chat_123",
  "history": [
    {
      "question": "What are our top-performing products this quarter?",
      "answer": "Based on your Q1 sales data, here are the top-performing products:\n\n1. **Product Alpha** - $2.1M revenue (15% growth)\n2. **Product Beta** - $1.8M revenue (8% growth)\n3. **Product Gamma** - $1.5M revenue (22% growth)",
      "timestamp": "2025-06-20T09:15:30"
    },
    {
      "question": "Can you break that down by region?",
      "answer": "Here's the regional breakdown for your top products:\n\n**North Region:**\n- Product Alpha: $850K\n- Product Beta: $720K\n- Product Gamma: $600K\n\n**South Region:**\n- Product Alpha: $1.25M\n- Product Beta: $1.08M\n- Product Gamma: $900K",
      "timestamp": "2025-06-20T09:18:45"
    },
    {
      "question": "Which region has the highest growth rate?",
      "answer": "The South Region shows the highest growth rate at 28% compared to the same period last year, while the North Region has a 12% growth rate.",
      "timestamp": "2025-06-20T09:22:10"
    }
  ]
}
```

#### Error Response

```json
{
  "status": "error",
  "message": "Chat history not found for the given chat_id"
}
```

### Response Fields

#### Success Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always "success" for successful requests |
| `chat_id` | `string` | The chat session identifier |
| `history` | `array` | Array of conversation messages |

#### History Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `question` | `string` | The user's question |
| `answer` | `string` | The agent's response |
| `timestamp` | `string` | When the exchange occurred (ISO 8601 format) |

### Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `"Chat history not found for the given chat_id"` | Invalid or non-existent chat ID | Verify the chat_id from the `/chats` endpoint |
| `"Database connection error"` | System issue | Try again later or contact support |
| `"Access denied"` | Insufficient permissions | Ensure you have access to this chat session |

---

## Workflow Examples

### Complete Chat Management Flow

```javascript
// 1. First, get all available chats
const chatsResponse = await fetch('/chats');
const chatsData = await chatsResponse.json();

console.log('Available chats:', chatsData.chats);

// 2. Select a specific chat and get its history
const selectedChatId = chatsData.chats[0].chat_id;
const historyResponse = await fetch(`/chat/${selectedChatId}/history`);
const historyData = await historyResponse.json();

console.log('Chat history:', historyData.history);

// 3. Continue the conversation
const followUpResponse = await fetch('/query/agent', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    agent_name: chatsData.chats[0].agent_name,
    question: 'Based on our previous discussion, what are the next steps?',
    chat_id: selectedChatId
  })
});
```

### Building a Chat Selection Interface

```javascript
async function loadChatSelector() {
  try {
    const response = await fetch('/chats');
    const data = await response.json();
    
    if (data.status === 'success') {
      const chatList = data.chats.map(chat => ({
        id: chat.chat_id,
        label: `${chat.agent_name} - ${new Date(chat.created_at).toLocaleDateString()}`,
        agent: chat.agent_name,
        created: chat.created_at
      }));
      
      return chatList;
    } else {
      console.error('Failed to load chats:', data.message);
      return [];
    }
  } catch (error) {
    console.error('Error loading chats:', error);
    return [];
  }
}

// Usage
const availableChats = await loadChatSelector();
console.log('Select from these chats:', availableChats);
```

### Finding Chats by Agent

```javascript
async function getChatsByAgent(agentName) {
  const response = await fetch('/chats');
  const data = await response.json();
  
  if (data.status === 'success') {
    return data.chats.filter(chat => chat.agent_name === agentName);
  }
  return [];
}

// Find all sales agent chats
const salesChats = await getChatsByAgent('sales_data_agent');
console.log('Sales agent conversations:', salesChats);
```

## Best Practices

### Chat Organization

**✅ Good Practices:**
- Use the `/chats` endpoint to get an overview before diving into specific conversations
- Group related conversations by agent type
- Keep track of important chat_id values for ongoing discussions
- Review recent chats before starting new conversations on similar topics

**❌ Avoid:**
- Creating too many short, disconnected conversations
- Mixing unrelated topics in the same chat session
- Forgetting to reference previous conversations when continuing analysis

### Efficient Chat Management

1. **Start with Overview**: Always check `/chats` to see existing conversations
2. **Reuse Existing Chats**: Continue relevant conversations instead of starting new ones
3. **Organize by Purpose**: Use different agents for different types of analysis
4. **Monitor Chat Volume**: Keep track of active conversations to avoid confusion

## Use Cases

### 📋 **Session Management**
```http
GET /chats
```
Get an overview of all your chat sessions to manage ongoing conversations.

### 🔄 **Continuing Conversations**
```http
GET /chat/auto_generated_chat_123/history
```
Review past conversations before asking follow-up questions.

### 📊 **Analytics & Reporting**
Analyze patterns in your agent interactions and conversation topics.

### 🎯 **Team Collaboration**
Share specific chat sessions with team members for collaborative analysis.

## Data Retention

:::tip
Chat sessions and history are preserved to maintain conversation context. Check your plan limits:

- **Free Plan**: 7 days retention
- **Pro Plan**: 30 days retention  
- **Enterprise Plan**: 90 days retention
:::

## Privacy & Security

- All chat data is tied to your account and agent sessions
- Only authorized users can access chat sessions and history
- Consider data sensitivity when storing conversation history
- Chat IDs are unique and cannot be guessed by unauthorized users

## Next Steps

After exploring your chats:

1. **Select Relevant Chats**: Choose conversations that relate to your current analysis needs
2. **Continue Conversations**: Use existing chat_id values to maintain context
3. **Organize by Agent**: Group conversations by agent type for better management
4. **Export Important Insights**: Save valuable conversations for future reference