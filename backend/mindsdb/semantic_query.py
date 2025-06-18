import mindsdb_sdk
from typing import Optional

# Connect to MindsDB
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

def semantic_search(content_column: Optional[str] = None):
    print(content_column)
    try:
        if content_column:
            # Search based on content column
            sql = f"""
                SELECT *
                FROM sales_data_kb
                WHERE content = '{content_column}'
            """
        else:
            # Return all data
            sql = """
                SELECT *
                FROM sales_data_kb
            """
            
        result = con.query(sql)
        return {
            "status": "success", 
            "data": result.fetch(),
            "search_type": "content_based" if content_column else "full"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
