import streamlit as st
import asyncio
import nest_asyncio
from index_code import create_index
from code_search import response

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

# Set up the Streamlit app
st.title("GitHub Repository Query Interface")

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

            # Assuming 'response' is an async function
            results = await response(index, query)
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
