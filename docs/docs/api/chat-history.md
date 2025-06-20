---
id: chat-history
title: Chat History
sidebar_label: Chat History
---

# Get Chat History

Retrieve the complete conversation history for a specific chat session with an AI agent.

## Overview

The Chat History endpoint allows you to access all questions and answers from a chat session. This is useful for reviewing past conversations, continuing discussions, or analyzing interaction patterns with your AI agents.

:::info
Chat history is automatically maintained when you use the Agent Q&A endpoint. Each chat session preserves the full conversation context.
:::

## Endpoint

```http
GET /chat/{chat_id}/history
```

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chat_id` | `string` | ✅ **Required** | The unique chat session identifier |

### Parameter Details

- **`chat_id`**: The unique identifier returned when you first query an agent or create a new chat session

## Example Request

```http
GET /chat/auto_generated_chat_123/history
```

## Response

### Success Response

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

### Error Response

```json
{
  "status": "error",
  "message": "Chat history not found for the given chat_id"
}
```

## Response Fields

### Success Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always "success" for successful requests |
| `chat_id` | `string` | The chat session identifier |
| `history` | `array` | Array of conversation messages |

### History Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `question` | `string` | The user's question |
| `answer` | `string` | The agent's response |
| `timestamp` | `string` | When the exchange occurred (ISO 8601 format) |

## Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `"Chat history not found for the given chat_id"` | Invalid or non-existent chat ID | Verify the chat_id or start a new conversation |
| `"Database connection error"` | System issue | Try again later or contact support |
| `"Access denied"` | Insufficient permissions | Ensure you have access to this chat session |

## Use Cases

### 📋 **Review Past Conversations**
```http
GET /chat/sales_analysis_chat_456/history
```
Perfect for reviewing what insights were discovered in previous sessions.

### 🔄 **Context for New Questions**
Check history before asking follow-up questions to understand what was already discussed.

### 📊 **Conversation Analysis**
Analyze patterns in questions and responses to improve your data queries.

### 🎯 **Training & Onboarding**
Show team members examples of effective questions and agent responses.

## Best Practices

### Managing Chat Sessions

**✅ Good Practices:**
- Keep chat_id values for important conversations
- Review history before asking follow-up questions
- Use descriptive chat sessions for different topics

**❌ Avoid:**
- Losing track of important chat_id values
- Mixing unrelated topics in the same chat
- Assuming context without checking history

### History Analysis

- **Look for Patterns**: Identify which types of questions get the best responses
- **Build on Previous Insights**: Use history to ask more targeted follow-up questions
- **Share Valuable Conversations**: Export useful Q&A sessions for team reference

## Integration Examples

### Continuing a Conversation

```javascript
// First, get the chat history
const historyResponse = await fetch('/chat/auto_generated_chat_123/history');
const history = await historyResponse.json();

// Review the last few exchanges
const recentHistory = history.history.slice(-3);
console.log('Recent conversation:', recentHistory);

// Then ask a follow-up question
const followUpResponse = await fetch('/query/agent', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    agent_name: 'sales_data_agent',
    question: 'Based on our previous discussion, what should we focus on next?',
    chat_id: 'auto_generated_chat_123'
  })
});
```

### Building a Chat Interface

```javascript
// Load existing conversation
async function loadChatHistory(chatId) {
  try {
    const response = await fetch(`/chat/${chatId}/history`);
    const data = await response.json();
    
    if (data.status === 'success') {
      return data.history;
    } else {
      console.error('Failed to load chat:', data.message);
      return [];
    }
  } catch (error) {
    console.error('Error loading chat history:', error);
    return [];
  }
}
```

## Data Retention

:::tip
Chat history is preserved to maintain conversation context. Check your plan limits for how long history is retained:

- **Free Plan**: 7 days
- **Pro Plan**: 30 days  
- **Enterprise Plan**: 90 days
:::

## Privacy & Security

- Chat history is tied to your account and agent sessions
- Only authorized users can access chat history
- Consider data sensitivity when storing conversation history

## Next Steps

After retrieving chat history:

1. **Continue Conversations**: Use the chat_id to ask follow-up questions
2. **Export Important Insights**: Save valuable Q&A sessions for reference
3. **Analyze Question Patterns**: Improve your questioning techniques
4. **Share with Team**: Use history to train others on effective agent interactions