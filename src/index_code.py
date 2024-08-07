
import os
import pymysql
from dotenv import load_dotenv
from transformers import LlamaTokenizer, LlamaModel
import torch
import ast
import hashlib
from llama_index.core import VectorStoreIndex, Settings
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# Load environment variables from .env file
load_dotenv()

# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

# Server-side: Use a pre-configured GitHub token (manage your pool of tokens)
# Ideally, this should be stored securely in an environment variable or a secure vault
github_token = os.getenv("GITHUB_TOKEN")  # Use your server-managed token here
    
# Initialize GitHub client and reader
github_client = GithubClient(github_token=github_token, verbose=False)
    


async def create_index(owner, repo):
    reader = GithubRepositoryReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        use_parser=True,  # Set to True if you want to parse the code for structure
        verbose=True
    )
    documents = reader.load_data(branch="main")
    index = VectorStoreIndex.from_documents(documents)
    return index
