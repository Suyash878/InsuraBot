import mindsdb_sdk
from typing import Optional

# Connect to MindsDB
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

def semantic_search(kb_name: str, content_column: Optional[str] = None):
    try:
        if content_column:
            sql = f"""
                SELECT *
                FROM {kb_name}
                WHERE content = '{content_column}'
            """
        else:
            sql = f"""
                SELECT *
                FROM {kb_name}
            """
        result = con.query(sql)
        return {
            "status": "success",
            "data": result.fetch(),
            "search_type": "content_based" if content_column else "full"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
