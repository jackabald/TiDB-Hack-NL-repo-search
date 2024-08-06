import os
import pymysql
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import torch

# Load environment variables from .env file
load_dotenv()

# TiDB connection details
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_PORT = int(os.getenv("TIDB_PORT"))
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")

# Connect to TiDB with SSL/TLS
connection = pymysql.connect(
    host=TIDB_HOST,
    port=TIDB_PORT,
    user=TIDB_USER,
    password=TIDB_PASSWORD,
    database=TIDB_DATABASE,
    ssl={'ssl': True} 
)

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/graphcodebert-base")
model = AutoModel.from_pretrained("microsoft/graphcodebert-base")

# Generate a vector for a given query to the chat bot
def generate_query_vector(query):
    inputs = tokenizer(query, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        vector = outputs.last_hidden_state.mean(dim=1).squeeze()
    return vector

# Search code snippets using TiDB's vector search capabilities
def search_code_snippets(query, top_k=5):
    query_vector = generate_query_vector(query)
    query_vector_json = json.dumps(query_vector.tolist())

    with connection.cursor() as cursor:
        sql = """
        SELECT file_path, function_name, type, start_line, end_line, code, vector, 
               COSINE_SIMILARITY(vector, %s) AS similarity
        FROM code_snippets
        ORDER BY similarity DESC
        LIMIT %s;
        """
        cursor.execute(sql, (query_vector_json, top_k))
        results = cursor.fetchall()

    snippets = []
    for result in results:
        snippets.append({
            "file_path": result[0],
            "function_name": result[1],
            "type": result[2],
            "start_line": result[3],
            "end_line": result[4],
            "code": result[5],
            "similarity": result[6]
        })

    return snippets