import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.vector_stores.tidbvector import TiDBVectorStore

# Load environment variables from .env file
load_dotenv()

# Initialize GitHub client
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GitHub token not found in environment variables.")
github_client = GithubClient(github_token=github_token, verbose=False)

# Initialize TiDB connection
tidb_connection_url = os.getenv("TIDB_URL")
if not tidb_connection_url:
    raise ValueError("TiDB connection URL not found in environment variables.")

async def create_index(owner, repo):
    try:
        # Initialize GitHub repository reader
        reader = GithubRepositoryReader(
            github_client=github_client,
            owner=owner,
            repo=repo,
            use_parser=True,
            verbose=True
        )
        
        # Load documents from the GitHub repository
        documents = reader.load_data(branch="main")

        # Initialize TiDB vector store
        tidbvec = TiDBVectorStore(
            connection_string=tidb_connection_url,
            table_name="repo_" + repo,
            distance_strategy="cosine",
            vector_dimension=768,
            drop_existing_table=False,
        )
        
        # Initialize storage context and index
        storage_context = StorageContext.from_defaults(vector_store=tidbvec)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )
        
        return index

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

