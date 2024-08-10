# Semantic Search Engine for Code Repositories   

## Overview  
The Semantic Search Engine for Code Repositories is an AI-powered tool designed to help developers find relevant code snippets, functions, or entire libraries based on natural language queries. By leveraging advanced NLP techniques, large language models (LLMs), and TiDB Serverless with Vector Search, this tool allows users to efficiently locate specific code patterns, structures, or algorithms within a codebase.

## Features
- Natural Language Querying: Search for code using plain English queries like "find the piece of code that initializes the BST" or "locate the function that performs quicksort."  
- Vector Search: Utilizes TiDB Serverless's Vector Search capabilities to identify and retrieve semantically similar code snippets.  
- File and Line Number Retrieval: Provides the exact file path and line number where the relevant code appears, along with a code snippet for context.  
- Contextual Understanding: Employs LLMs to understand the context and intent behind queries, making the search highly accurate and intuitive.  
- Code Reuse Encouragement: Facilitates code reuse by making it easy to find existing solutions, reducing redundancy in development.  


## Prerequisites  
Before you begin, ensure you have the following installed on your machine:  
- Python 3.8+
- Git
- Virtual Environment (Optional but recommended)  
You'll also need:  
- A TiDB Cloud account and a Serverless instance set up. 
   
## Installation  
1. Clone the Repository  
```bash
git clone https://github.com/jackabald/TiDB-Hack-NL-repo-search.git  
cd TiDB-Hack-NL-repo-search`
```
2. Set Up a Virtual Environment (Optional but Recommended)  
```bash
python -m venv venv  
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install Dependencies  
```bash
pip install -r requirements.txt
```
4. Insall Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
5. Configure Environment Variables  
```
TIDB_URL="<your-tidb-pymysql>"
GITHUB_TOKEN="<your-github-token>"
JINA_API_KEY="<your-jina-api-key>
```
Replace the placeholders with your actual TiDB and GitHub credentials.
