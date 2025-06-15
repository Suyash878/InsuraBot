import mindsdb_sdk
con = mindsdb_sdk.connect()
con = mindsdb_sdk.connect('http://127.0.0.1:47334')

databases = con.databases.list()

database = databases[0]

query = con.query("""
CREATE KNOWLEDGE_BASE text_case_kb
USING
    embedding_model = {
        "provider": "gemini",
        "model_name" : "text-embedding-004",
        "api_key": "AIzaSyBcRaIybCZm9R2aDsU-yePHdiHeblwO4BM"
    },
    reranking_model = {
        "provider": "together_ai",
        "model_name": "Salesforce/Llama-Rank-V1",
        "api_key": "4903bdc4bd98583e8158c62c0b0a496b0c5d4b7c8143fcca1821736ff335f7fa"
    },
    metadata_columns = ['sales_rep'],
    content_columns = ['region'],
    id_column = 'transaction_id';""")

print(query.fetch())