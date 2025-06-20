from mindsdb_sdk import connect
from typing import List, Optional
from pydantic import BaseModel, Field

class CreateJobRequest(BaseModel):
    job_name: str = Field(..., description="Unique job name")
    source_table: str = Field(..., description="Fully qualified source table name (e.g. db.table)")
    kb_name: str = Field(..., description="Knowledge Base name to insert into")
    content_columns: List[str] = Field(..., description="Columns to copy into the KB")
    filter_column: str = Field(..., description="Column used to detect new rows (e.g., created_at or id)")
    interval: str = Field("10 MINUTES", description="Job interval (e.g., '5 MINUTES')")
    start_time: Optional[str] = Field(None, description="Start time (e.g., '2025-06-19 18:00:00')")
    end_time: Optional[str] = Field(None, description="End time")

class JobManager:
    def __init__(self):
        self.con = connect("http://127.0.0.1:47334")

    def create_job(self, payload: CreateJobRequest) -> dict:
        filter_clause = f"WHERE {payload.filter_column} > (SELECT MAX({payload.filter_column}) FROM LAST('{payload.kb_name}'))"
        selected_columns = ", ".join(payload.content_columns)

        sql_parts = [f"CREATE JOB {payload.job_name}"]
        if payload.start_time:
            sql_parts.append(f"START '{payload.start_time}'")
        if payload.end_time:
            sql_parts.append(f"END '{payload.end_time}'")
        sql_parts.append(f"EVERY {payload.interval}")
        sql_parts.append(f"""
        IF (
            SELECT * FROM {payload.source_table}
            {filter_clause}
        )
        INSERT INTO {payload.kb_name}
            SELECT {selected_columns}
            FROM {payload.source_table}
            {filter_clause};
        """)

        final_sql = "\n".join(sql_parts)

        try:
            self.con.query(final_sql).fetch()
            return {
                "status": "success",
                "message": f"Job `{payload.job_name}` created successfully.",
                "sql": final_sql
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "sql": final_sql
            }
