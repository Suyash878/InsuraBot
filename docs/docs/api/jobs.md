---
id: jobs
title: Jobs API
sidebar_label: Jobs
---

# Jobs API

The Jobs API allows you to create and manage scheduled synchronization jobs that automatically sync data from source tables to knowledge bases at regular intervals.

## Overview

Jobs provide an automated way to keep your knowledge bases up-to-date by continuously syncing data from your database tables. You can configure filters, specify content columns, and set custom schedules to meet your data synchronization needs.

---

## Create a Job

Creates a new scheduled job to sync data from a source table to a knowledge base.

### Endpoint

```http
POST /jobs/create
```

### Request Body

The request body should contain a JSON object with the following properties:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_name` | `string` | ✅ | Unique identifier for the job |
| `source_table` | `string` | ✅ | Source table in format `database.table` |
| `kb_name` | `string` | ✅ | Target knowledge base name |
| `content_columns` | `array<string>` | ✅ | Columns to include in the sync |
| `filter_column` | `string` | ✅ | Column used for filtering data |
| `interval` | `string` | ✅ | Sync frequency (e.g., "10 MINUTES", "1 HOUR") |
| `start_time` | `string` | ✅ | Job start time in ISO format |
| `end_time` | `string` | ✅ | Job end time in ISO format |

### Example Request

```json
{
  "job_name": "sync_orders",
  "source_table": "orders_db.orders",
  "kb_name": "orders_kb",
  "content_columns": ["product", "description"],
  "filter_column": "created_at",
  "interval": "10 MINUTES",
  "start_time": "2025-06-19T18:00:00",
  "end_time": "2025-06-20T18:00:00"
}
```

### Response

#### Success Response

**Status Code:** `201 Created`

```json
{
  "success": true,
  "message": "Job created successfully",
  "data": {
    "job_id": "job_12345",
    "job_name": "sync_orders",
    "status": "scheduled",
    "created_at": "2025-06-19T12:00:00Z",
    "next_run": "2025-06-19T18:00:00Z"
  }
}
```

#### Error Response

**Status Code:** `400 Bad Request`

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid job configuration",
    "details": [
      "job_name is required",
      "invalid interval format"
    ]
  }
}
```

### cURL Example

```bash
curl -X POST "http://127.0.0.1:8000/jobs/create" \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "sync_orders",
    "source_table": "orders_db.orders",
    "kb_name": "orders_kb",
    "content_columns": ["product", "description"],
    "filter_column": "created_at",
    "interval": "10 MINUTES",
    "start_time": "2025-06-19T18:00:00",
    "end_time": "2025-06-20T18:00:00"
  }'
```

### Python Example

```python
import requests
import json

url = "http://127.0.0.1:8000/jobs/create"
payload = {
    "job_name": "sync_orders",
    "source_table": "orders_db.orders",
    "kb_name": "orders_kb",
    "content_columns": ["product", "description"],
    "filter_column": "created_at",
    "interval": "10 MINUTES",
    "start_time": "2025-06-19T18:00:00",
    "end_time": "2025-06-20T18:00:00"
}

response = requests.post(url, json=payload)
print(response.json())
```

### JavaScript Example

```javascript
const response = await fetch('http://127.0.0.1:8000/jobs/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    job_name: 'sync_orders',
    source_table: 'orders_db.orders',
    kb_name: 'orders_kb',
    content_columns: ['product', 'description'],
    filter_column: 'created_at',
    interval: '10 MINUTES',
    start_time: '2025-06-19T18:00:00',
    end_time: '2025-06-20T18:00:00'
  })
});

const data = await response.json();
console.log(data);
```

---

## Interval Formats

The `interval` parameter accepts various time formats:

| Format | Description | Example |
|--------|-------------|---------|
| `X MINUTES` | Every X minutes | `"5 MINUTES"`, `"30 MINUTES"` |
| `X HOURS` | Every X hours | `"1 HOUR"`, `"6 HOURS"` |
| `X DAYS` | Every X days | `"1 DAY"`, `"7 DAYS"` |
| `HOURLY` | Every hour | `"HOURLY"` |
| `DAILY` | Every day | `"DAILY"` |
| `WEEKLY` | Every week | `"WEEKLY"` |

---

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Request body validation failed |
| `DUPLICATE_JOB` | Job with the same name already exists |
| `INVALID_TABLE` | Source table does not exist or is inaccessible |
| `INVALID_KB` | Knowledge base does not exist |
| `INVALID_INTERVAL` | Interval format is not supported |
| `INVALID_DATETIME` | Start or end time format is invalid |

---

## Notes

- Job names must be unique across the system
- The `start_time` and `end_time` should be in ISO 8601 format
- Jobs will automatically stop running after the `end_time`
- The `filter_column` is typically a timestamp column used to identify new or updated records
- All specified `content_columns` must exist in the source table

---

## Rate Limits

- Maximum of 100 active jobs per account
- Minimum interval is 1 minute
- Maximum job duration is 30 days