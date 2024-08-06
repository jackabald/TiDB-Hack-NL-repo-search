import streamlit as st
import os
import zipfile
import tempfile

# Import the functions from the code_search.py and index_code.py files
from index_code import index_code_directory
from code_search import search_code_snippets

# Set up the Streamlit app
st.title("Project Folder Upload and Query Interface")

# File uploader for the project folder
uploaded_file = st.file_uploader("Upload your project (zip format)", type="zip")

# Text box for the query
query = st.text_input("Enter your query")

# Button to submit the query
if st.button("Submit Query"):
    if uploaded_file is not None:
        # Save the uploaded zip file to a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, uploaded_file.name)
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract the zip file
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(tmpdir)
            
            # Index the extracted folder
            st.info("Indexing code files in the uploaded folder...")
            index_code_directory(tmpdir)  # Calls your function to index the code directory
            
            st.success("Folder indexed successfully!")
            
            # Here you can proceed with querying or any other operation after indexing
            results = search_code_snippets(query)
            st.write(results)

    else:
        st.error("Please upload a project folder and enter a query.")