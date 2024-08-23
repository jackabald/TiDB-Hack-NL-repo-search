import streamlit as st
import nest_asyncio
from rag import create_index, response
from components.sidebar import side_info
from components.utils import initialize_session_state

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

# Set up the Streamlit app
st.title("🔍: GitHub Repository RAG")
# st.set_page_config(page_title="Codebase AI", page_icon="🌟")
side_info()
initialize_session_state()

# Input for the GitHub repository URL
repo_url = st.text_input("Enter GitHub repository URL (e.g., https://github.com/owner/repo)")

# Handle repository indexing separately
def handle_repo(repo_url):
    if repo_url:
        try:
            # Extract owner and repo name from the URL
            owner, repo = repo_url.rstrip("/").split("/")[-2:]

            # Check if repository has changed
            st.info("Wait! Fetching and indexing repository from GitHub...")
            index = create_index(owner, repo)
            if index:
                st.session_state.index = index
                st.session_state.repo_name = repo
                st.success("Repository indexed successfully.")
                st.info("You can now start querying the repository.")
            else:
                st.error("Failed to index the repository.")
        except Exception as e:
            st.error(f"An error occurred while indexing: {str(e)}")
    else:
        st.error("Please enter a GitHub repository URL.")

# Ensure the repository is handled only once
if 'index' not in st.session_state:
    handle_repo(repo_url)

# Function to process user queries
def process_query(query):
    if st.session_state.index is None:
        st.error("Repository not indexed yet. Please enter a valid GitHub repository URL.")
        return None

    try:
        st.info("Querying for results...")
        results = response(st.session_state.index, query)
        return results
    except Exception as e:
        st.error(f"An error occurred while querying: {str(e)}")
        return None
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if usr_input := st.chat_input("Enter your query"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": usr_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(usr_input)

    # Process the query and display assistant response
    with st.chat_message("assistant"):
        if results := process_query(usr_input):
            # Display the results
            st.markdown(results)
            st.session_state.messages.append({"role": "assistant", "content": results})
        else:
            st.error("Failed to get a response. Please check the repository URL and query.")
