# We are using the GraphCodeBERT model to generate vectors for code snippets.
# The vectors are stored in a TiDB database along with metadata such as file path, function name, etc.
# We are using GraphCodeBERT because of its specialized architecture for code.

import os
import pymysql
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import torch
import ast
import hashlib

# Load environment variables from .env file
load_dotenv()

# TiDB connection details
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_PORT = int(os.getenv("TIDB_PORT"))
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")

# Connect to TiDB
connection = pymysql.connect(
    host=TIDB_HOST,
    port=TIDB_PORT,
    user=TIDB_USER,
    password=TIDB_PASSWORD,
    database=TIDB_DATABASE,
    ssl = {'ssl': True}
)

# Load GraphCodeBERT
tokenizer = AutoTokenizer.from_pretrained("microsoft/graphcodebert-base")
model = AutoModel.from_pretrained("microsoft/graphcodebert-base")

# Create SQL table if it does not exist
def create_table_if_not_exists():
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS code_snippets (
            id INT PRIMARY KEY AUTO_INCREMENT,
            file_hash VARCHAR(32),
            file_path VARCHAR(255),
            function_name VARCHAR(255),
            type VARCHAR(50),
            start_line INT,
            end_line INT,
            code TEXT,
            vector JSON
        );
        """)
        connection.commit()

# Extract code structures
def extract_code_snippets(file_path):
    with open(file_path, "r") as file:
        code = file.read()
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return []

    snippets = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            start_line = node.lineno
            end_line = node.body[-1].lineno
            snippet = {
                "name": node.name,
                "type": type(node).__name__,
                "start_line": start_line,
                "end_line": end_line,
                "code": ast.get_source_segment(code, node)
            }
            snippets.append(snippet)
    return snippets

# Generate vectors using GraphCodeBERT
def generate_graphcodebert_vector(code_snippet):
    inputs = tokenizer(code_snippet, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        vector = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return vector

# Create metadata for each code snippet including its vector
def create_vector_metadata(code_snippets):
    vector_metadata = []
    for snippet in code_snippets:
        vector = generate_graphcodebert_vector(snippet["code"])
        vector_metadata.append({
            "name": snippet["name"],
            "type": snippet["type"],
            "vector": vector.tolist(),  # Ensure vector is a list, which is JSON-serializable
            "start_line": snippet["start_line"],
            "end_line": snippet["end_line"],
            "code": snippet["code"]
        })
    return vector_metadata

# Store vectors and metadata in TiDB
def store_in_tidb(file_path, vectors):
    create_table_if_not_exists()  # Ensure the table exists
    with connection.cursor() as cursor:
        for item in vectors:
            file_hash = hashlib.md5(file_path.encode()).hexdigest()
            sql = """
            INSERT INTO code_snippets (file_hash, file_path, function_name, type, start_line, end_line, code, vector)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                file_hash,
                file_path,
                item["name"],
                item["type"],
                item["start_line"],
                item["end_line"],
                item["code"],
                str(item["vector"])
            ))
        connection.commit()

# Index code files in the directory
def index_code_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # TODO: extend this to other languages
                file_path = os.path.join(root, file)
                print(f"Indexing {file_path}...")
                snippets = extract_code_snippets(file_path)
                vectors = create_vector_metadata(snippets)
                store_in_tidb(file_path, vectors)