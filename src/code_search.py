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

# Function to generate a vector for a given query
def generate_query_vector(query):
    inputs = tokenizer(query, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        vector = outputs.last_hidden_state.mean(dim=1).squeeze()
    return vector

# Function to search code snippets using TiDB's vector search capabilities
def search_code_snippets(query, top_k=1):
    query_vector = generate_query_vector(query).numpy().reshape(1, -1)  # Ensure query_vector is 2D

    with connection.cursor() as cursor:
        sql = """
        SELECT file_path, function_name, type, start_line, end_line, code, vector
        FROM code_snippets
        """
        cursor.execute(sql)
        results = cursor.fetchall()

    snippets = []
    vectors = []

    # Parse the results and calculate cosine similarity
    for result in results:
        vector = np.array(json.loads(result[6])).flatten()  # Ensure the vector is 1D
        vectors.append((result, vector))

    if vectors:
        # Create a 2D array with each vector being a row
        vector_array = np.vstack([v[1] for v in vectors])  # Ensure a 2D array
        similarities = cosine_similarity(query_vector, vector_array).flatten()

        # Sort by similarity and pick the top_k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        for index in top_indices:
            result = vectors[index][0]
            snippets.append({
                "file_path": result[0],
                "function_name": result[1],
                "type": result[2],
                "start_line": result[3],
                "end_line": result[4],
                "code": result[5],
                "similarity": similarities[index]
            })

    return snippets