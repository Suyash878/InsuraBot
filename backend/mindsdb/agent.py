import mindsdb_sdk
import pandas as pd
from typing import Optional

# Connect to MindsDB
con = mindsdb_sdk.connect("http://127.0.0.1:47334")

# Configure pandas display options globally
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

def query_agent(agent_name: str, question: str) -> dict:
    """
    Query a MindsDB agent with a specific question using pandas for response handling
    
    Args:
        agent_name (str): Name of the agent to query
        question (str): Question to ask the agent
    """
    try:
        query = f"""
        SELECT answer
        FROM {agent_name}
        WHERE question = '{question}';
        """
        
        result = con.query(query)
        df = pd.DataFrame(result.fetch())
        
        if df.empty:
            return {
                "status": "error",
                "message": "No response received from agent"
            }
            
        return {
            "status": "success",
            "agent": agent_name,
            "question": question,
            "answer": df['answer'].values[0]  # Get full, untruncated answer
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}