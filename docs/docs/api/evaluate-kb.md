---
id: evaluate-kb
title: Evaluate Knowledge Base
sidebar_label: Evaluate KB
---

# Evaluate a Knowledge Base

Evaluate the quality and performance of a registered knowledge base using an LLM.

## Overview

This endpoint allows you to trigger an evaluation of a knowledge base, optionally specifying LLM provider, model, and other parameters. The evaluation can help you understand how well your knowledge base can answer questions or perform semantic tasks.

---

## Endpoint

```http
POST /evaluate-kb
```

## Request Body

| Parameter   | Type    | Required | Description                                                      |
|-------------|---------|----------|------------------------------------------------------------------|
| `kb_name`   | string  | ✅       | Name of the knowledge base to evaluate                           |
| `evaluate`  | boolean | ❌       | Whether to run evaluation (default: true)                        |
| `llm`       | object  | ❌       | LLM config: provider, model_name, api_key, base_url, api_version |

### LLM Object Fields

| Field        | Type   | Required | Description                                 |
|--------------|--------|----------|---------------------------------------------|
| provider     | string | ❌       | LLM provider (default: "gemini")            |
| model_name   | string | ❌       | Model name (default: "gemini-2.0-flash")    |
| api_key      | string | ❌       | API key for the LLM provider                |
| base_url     | string | ❌       | Custom base URL for the LLM API             |
| api_version  | string | ❌       | API version (default: "2024-02-01")         |
| method       | string | ❌       | Evaluation method (default: "multi-class")   |

## Example Request

```json
{
  "kb_name": "customer_orders_kb",
  "evaluate": true,
  "llm": {
    "provider": "gemini",
    "model_name": "gemini-2.0-flash",
    "api_key": "YOUR_API_KEY"
  }
}
```

## Response

### Success

```json
{
  "status": "success",
  "result": { /* evaluation results */ }
}
```

### Error

```json
{
  "status": "error",
  "message": "Error message"
}
```

## Notes

- If `evaluate` is false, only the evaluation setup is performed.
- If no `llm` is provided, defaults are used.
- Requires a valid knowledge base name.

---

## Example Python Usage

```python
import requests

payload = {
    "kb_name": "customer_orders_kb",
    "evaluate": True,
    "llm": {
        "provider": "gemini",
        "model_name": "gemini-2.0-flash",
        "api_key": "YOUR_API_KEY"
    }
}
response = requests.post("http://localhost:8000/evaluate-kb", json=payload)
print(response.json())
```