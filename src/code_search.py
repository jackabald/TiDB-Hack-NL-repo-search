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

# Load GraphCodeBERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/graphcodebert-base")
model = AutoModel.from_pretrained("microsoft/graphcodebert-base")

# TODO use gen-ai if needed and sql query
def search_code(codebase_path):
    results = []
    
    # Iterate through all files in the codebase
    for root, files in os.walk(codebase_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Extract code snippets from the file
            snippets = extract_code_snippets(file_path)
            
            # Add the file path and relevant information to the results
            result = {
                'file_path': file_path,
                'snippet': snippets,
                'explanation': 'This is a relevant code snippet for the query.'
            }
            results.append(result)
    return results

# Generate vector for query
def generate_query_vector(query):
    inputs = tokenizer(query, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        vector = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return vector
