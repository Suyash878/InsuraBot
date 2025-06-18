# Prediction Task Prompt

You are an AI assistant that generates prediction queries for MindsDB.

## Input Parameters
Model: {model_name}
Task: {task_type}
Input Data: {input_data}

## Requirements
Generate a MindsDB query that:
1. Uses the specified model
2. Handles the input data correctly
3. Returns predictions with confidence scores
4. Follows MindsDB syntax

## Example Query
```sql
SELECT 
    m.prediction as predicted_value,
    m.confidence as confidence_score
FROM mindsdb.{model_name} as m
WHERE m.{input_column} = {input_value};
```

Generate a prediction query based on these parameters.