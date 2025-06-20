---
id: register-sheet
title: Register Sheet
sidebar_label: Register Sheet
---

# Register a Google Sheet

Register a Google Sheet as a knowledge base and agent with our API.

## Overview

The Register Sheet endpoint allows you to integrate Google Sheets into your knowledge base system. You can specify metadata columns, content columns, and provide descriptions to help the system understand and process your data effectively.

:::info
Each sheet registration requires a unique identifier. Make sure to use descriptive IDs that help you manage multiple sheet registrations.
:::

## Endpoint

```http
POST /register-sheet
```

## Request Body

The request body should be a JSON object with the following properties:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ **Required** | Unique identifier for the sheet registration |
| `spreadsheet_id` | `string` | ✅ **Required** | Google Spreadsheet ID (found in the sheet URL) |
| `sheet_name` | `string` | ✅ **Required** | Name of the specific sheet tab within the spreadsheet |
| `data_description` | `string` | ❌ Optional | Human-readable description of what the data represents |
| `metadata_columns` | `string[]` | ❌ Optional | Array of column names that contain metadata information |
| `content_columns` | `string[]` | ❌ Optional | Array of column names that contain the main content data |

### Field Details

- **`id`**: Use a descriptive, unique identifier (e.g., `customer-orders-2024`, `product-catalog-main`)
- **`spreadsheet_id`**: Extract this from your Google Sheets URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`
- **`sheet_name`**: The tab name at the bottom of your Google Sheet
- **`data_description`**: Helps the system understand the context and purpose of your data
- **`metadata_columns`**: Columns containing organizational or categorical information
- **`content_columns`**: Columns containing the primary data you want to query against

## Example Request

```json
{
  "id": "customer-orders-q1",
  "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
  "sheet_name": "Q1_Orders",
  "data_description": "Customer transaction records for Q1 2024 including order details and sales metrics",
  "metadata_columns": ["sales_rep", "region", "order_date"],
  "content_columns": ["product_name", "product_description", "customer_feedback"]
}
```

## Response

### Success Response

```json
{
  "success": true,
  "message": "Sheet registered successfully",
  "id": "customer-orders-q1",
  "status": "active"
}
```

### Error Response

```json
{
  "success": false,
  "error": "Invalid spreadsheet ID or insufficient permissions",
  "code": "SHEET_ACCESS_ERROR"
}
```

## Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `SHEET_ACCESS_ERROR` | Cannot access the Google Sheet | Verify the spreadsheet ID and ensure proper sharing permissions |
| `DUPLICATE_ID` | The provided ID already exists | Use a different unique identifier |
| `INVALID_SHEET_NAME` | Sheet name not found in spreadsheet | Check that the sheet tab name matches exactly |
| `MISSING_REQUIRED_FIELDS` | Required fields are missing | Ensure `id`, `spreadsheet_id`, and `sheet_name` are provided |

## Best Practices

### Naming Conventions
- Use descriptive IDs: `product-inventory-main` instead of `sheet1`
- Include dates or versions when relevant: `sales-data-2024-q1`

### Column Selection
- **Metadata columns**: Choose columns that help categorize or filter your data
- **Content columns**: Select columns with rich, searchable content that users will query

### Data Description
Write clear, concise descriptions that explain:
- What the data represents
- The time period it covers
- Any important context about the data structure

## Prerequisites

Before registering a sheet, ensure:

1. **Google Sheet Access**: The sheet must be accessible with proper permissions
2. **Sheet Structure**: Your sheet should have clear column headers
3. **Data Quality**: Clean, well-formatted data produces better results

:::tip
Test your sheet registration with a small dataset first to ensure the column mappings work as expected.
:::

## Next Steps

After successfully registering your sheet:

1. **Query the Data**: Use the query endpoints to search and retrieve information
2. **Monitor Usage**: Check logs and analytics to understand how your data is being accessed
3. **Update as Needed**: Re-register with updated column mappings or descriptions as your data evolves