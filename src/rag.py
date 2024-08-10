from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.vector_stores.tidbvector import TiDBVectorStore
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
import streamlit as st

def initialize():
    """
    Initialize the configurations and clients using Streamlit secrets and session state.

    This function sets up the GitHub client, TiDB connection, Jina embedding model, and LLM.
    It handles the input of credentials and configurations from Streamlit's secrets or sidebar inputs.
    """
    # Initialize GitHub client
    if "GITHUB_TOKEN" in st.secrets:
        github_token = st.secrets["GITHUB_TOKEN"]
    else:
        raise ValueError("GitHub token not found in secrets.")

    github_client = GithubClient(github_token=github_token, verbose=False)

    # Initialize TiDB connection
    if "TIDB_URL" in st.secrets:
        tidb_connection_url = st.secrets["TIDB_URL"]
    elif "tidb_url" in st.session_state:
        tidb_connection_url = st.session_state.tidb_url
    else:
        st.warning('Please provide TiDB URL in the sidebar.', icon="⚠️")
        st.stop()

    # Initialize Jina Embedding Model
    if "JINA_API_KEY" in st.secrets:
        jinaai_api_key = st.secrets["JINA_API_KEY"]
    elif "jina_api_key" in st.session_state:
        jinaai_api_key = st.session_state.jina_api_key
    else:
        st.warning('Please provide Jina API key in the sidebar.', icon="⚠️")
        st.stop()

    Settings.embed_model = JinaEmbedding(
        api_key=jinaai_api_key,
        model="jina-embeddings-v2-base-en"
    )

    # Initialize LLM
    if "llm" not in st.session_state:
        st.session_state.llm = None

    if "OLLAMA_SERVER_URL" in st.secrets:
        ollama_server_url = st.secrets["OLLAMA_SERVER_URL"]
        st.session_state.ollama_server_url = ollama_server_url
    else:
        raise ValueError("Ollama server URL not found in secrets.")

    Settings.llm = Ollama(model="llama3", request_timeout=360.0)

    return github_client, tidb_connection_url

async def create_index(owner, repo):
    try:
        # Initialize GitHub repository reader
        github_client, tidb_connection_url = initialize()
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


# https://docs.pingcap.com/tidbcloud/vector-search-integrate-with-llamaindex
# TODO: research metadata filters and possible use them if they make results better
def response (index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response
