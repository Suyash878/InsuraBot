import mindsdb_sdk
from typing import Optional

# Connect to MindsDB
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

def semantic_search( content_column: str):
    try:
        sql = f"""
                    SELECT *
                    FROM insurance_kb
                    WHERE content = '{content_column}'
                """   
        result = con.query(sql)
        print(result.fetch())
        return {"status": "success", "data": result.fetch_all()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
