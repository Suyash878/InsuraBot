import mindsdb_sdk
import os

con = mindsdb_sdk.connect("http://127.0.0.1:47334")
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def evaluate_kb(
    kb_name: str,
    evaluate: bool = True,
    llm: dict = None
):
    try:
        eval_clause = "" if evaluate else "EVALUATE = false,"
        llm_clause = ""
        if llm:
            llm_clause = f"""
            llm = {{
                "provider": "{llm.get('provider', 'gemini')}",
                "model_name": "{llm.get('model_name', 'gemini-2.0-flash')}",
                "api_key": "{llm.get('api_key', GEMINI_API_KEY)}",
                "base_url": "{llm.get('base_url', '')}",
                "api_version": "{llm.get('api_version', '2024-02-01')}",
                "method": "{llm.get('method', 'multi-class')}"
            }},
            """
        query = f"""
        EVALUATE KNOWLEDGE_BASE {kb_name}
        USING
            {eval_clause}
            {llm_clause}
        ;
        """
        result = con.query(query)
        return {"status": "success", "result": result.fetch()}
    except Exception as e:
        return {"status": "error", "message": str(e)}