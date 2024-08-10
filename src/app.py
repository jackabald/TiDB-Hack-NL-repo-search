import streamlit as st
import asyncio
import nest_asyncio
from rag import create_index, response
from components.sidebar import side_info
from components.utils import initialise_session_state, clear_chat_history, abort_chat

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

# Set up the Streamlit app
st.title("🔍: GitHub Repository Query Interface")
# st.set_page_config(page_title="GitPilot AI", page_icon="🌟")
side_info()
initialise_session_state()

# Input for the GitHub repository URL
repo_url = st.text_input("Enter GitHub repository URL (e.g., https://github.com/owner/repo)")

# Text box for the query
query = st.text_input("Enter your query")

# Define an async function to handle the process
async def handle_query(repo_url, query):
    if repo_url:
        try:
            # Extract owner and repo name from the URL
            owner, repo = repo_url.rstrip("/").split("/")[-2:]

            st.info("Fetching and indexing repository from GitHub...")
            index = await create_index(owner, repo)
            
            if index:
                st.info("Querying for results...")
            # Assuming 'response' is an async function
            results = response(index, query)
            return results

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None
    else:
        st.error("Please enter a GitHub repository URL.")
        return None

# Run the async function using asyncio.run()
if st.button("Submit Query"):
    results = asyncio.run(handle_query(repo_url, query))
    if results:
        st.write(results)
