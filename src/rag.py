import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.readers.github import GithubRepositoryReader, GithubClient, GitHubRepositoryIssuesReader, GitHubIssuesClient
from llama_index.vector_stores.tidbvector import TiDBVectorStore
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

# Load environment variables from .env file
load_dotenv()

# Initialize GitHub client
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GitHub token not found in environment variables.")
github_client = GithubClient(github_token=github_token, verbose=False)
github_issues_client = GitHubIssuesClient(github_token=github_token, verbose=False)


# Initialize TiDB connection
tidb_connection_url = os.getenv("TIDB_URL")
if not tidb_connection_url:
    raise ValueError("TiDB connection URL not found in environment variables.")

# Initialize Jina Embedding Model
jinaai_api_key = os.getenv("JINA_API_KEY")
Settings.embed_model = JinaEmbedding(
    api_key=jinaai_api_key,
    model="jina-embeddings-v2-base-en"
)

# initialize llm
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

async def create_index(owner, repo):
    try:
        # Initialize GitHub repository reader
        reader = GithubRepositoryReader(
            github_client=github_client,
            owner=owner,
            repo=repo,
            use_parser=False,
            verbose=False
        )
        # Initialize GitHub issues reader
        issues_reader = GitHubRepositoryIssuesReader(
            github_client=github_issues_client,
            owner=owner,
            repo=repo,
            verbose=False
        )
        # Load documents from the GitHub repository
        documents = reader.load_data(branch="main")
        # Load issues from the GitHub repository
        issues = issues_reader.load_data(
            state=GitHubRepositoryIssuesReader.IssueState.ALL,
        )
        # Combine the documents and issues
        data = documents + issues
        
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
            data, storage_context=storage_context, show_progress=True
        )
        
        return index
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# https://docs.pingcap.com/tidbcloud/vector-search-integrate-with-llamaindex
# TODO: research metadata filters and possible use them if they make results better
def response (index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response