from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama


# TODO: Change to Jina code embedding model (hackathon sponsor and a judge is from Jina)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# initialize llm
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

# https://docs.pingcap.com/tidbcloud/vector-search-integrate-with-llamaindex
# TODO: research metadata filters and possible use them if they make results better
def response (index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response