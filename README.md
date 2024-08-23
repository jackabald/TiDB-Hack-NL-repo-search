<p align="center">
<img src="https://raw.githubusercontent.com/jackabald/TiDB-Hack-NL-repo-search/main/src/assets/codebaseai.png" height="130" alt="Codebase AI" />
</p>

<p align="center" style="margin-bottom: 50px">
<a href="https://github.com/jackabald/TiDB-Hack-NL-repo-search/issues">
        <img src="https://img.shields.io/github/issues/jackabald/TiDB-Hack-NL-repo-search" alt="Issues"></a>
    <a href="https://github.com/jackabald/TiDB-Hack-NL-repo-search/network/members" alt="Forks">
        <img src="https://img.shields.io/github/forks/jackabald/TiDB-Hack-NL-repo-search" /></a>
    <a href="https://github.com/jackabald/TiDB-Hack-NL-repo-search/stargazers" alt="Stars">
        <img src="https://img.shields.io/github/stars/jackabald/TiDB-Hack-NL-repo-search" /></a>
    <a href="https://github.com/jackabald/TiDB-Hack-NL-repo-search/graphs/contributors">
        <img src="https://img.shields.io/github/contributors/jackabald/TiDB-Hack-NL-repo-search"
            alt="Contributors"></a>
    <a href="https://github.com/jackabald/TiDB-Hack-NL-repo-search/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/jackabald/TiDB-Hack-NL-repo-search"
        alt="License"></a>
    <a href="https://docs.pingcap.com/tidbcloud/">
        <img src="https://img.shields.io/badge/-TiDB%20Cloud-orange"
            alt="TiDB Cloud"/></a>
</p>

# Table of contents

<!--ts-->
   * [Project Overview](#Overview)
   * [Features](#Features)
      * [App Architecture](#App-Architecture) :TODO
   * [Prerequisites](#Prerequisites)
   * [Project Setup](#Installation)
   * [Contributing](#Contributing)
   * [How to get started with TiDB Vectors](#How-to-get-started-with-TiDB Vectors) :TODO
<!--te-->


## Overview  
The Semantic Search Engine for Code Repositories is an AI-powered tool designed to help developers find relevant code snippets, functions, or entire libraries based on natural language queries. By leveraging advanced NLP techniques, large language models (LLMs), and TiDB Serverless with Vector Search, this tool allows users to efficiently locate specific code patterns, structures, or algorithms within a codebase.

## Features
- Natural Language Querying: Search for code using plain English queries like "find the piece of code that initializes the BST" or "locate the function that performs quicksort."  
- Vector Search: Utilizes TiDB Serverless's Vector Search capabilities to identify and retrieve semantically similar code snippets.  
- File and Line Number Retrieval: Provides the exact file path and line number where the relevant code appears, along with a code snippet for context.  
- Contextual Understanding: Employs LLMs to understand the context and intent behind queries, making the search highly accurate and intuitive.  
- Code Reuse Encouragement: Facilitates code reuse by making it easy to find existing solutions, reducing redundancy in development.  


## Prerequisites 🛠️
Before you begin, ensure you have the following installed on your machine:  
- Python 3.8+
- Git
- Virtual Environment (Optional but recommended)  
You'll also need:  
- A TiDB Cloud account and a Serverless instance set up. 
   
## Installation ⚙️
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
4. Install, configure Ollama and connect to large language models via the Ollama server.
- [Setup Ollama](./docs/OLLAMA.md)

6. Set up your `secrets.toml` file under `.streamlit` directory and copy `example.secrets.toml` into `secrets.toml` and replace the keys
```
TIDB_URL="<your-tidb-pymysql>"
GITHUB_TOKEN="<your-github-token>"
JINA_API_KEY="<your-jina-api-key>"
```

## Contributing 🤝
Contributions to this project are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the project's GitHub repository.

## License 📝
This project is licensed under the [Apache License](https://github.com/jackabald/TiDB-Hack-NL-repo-searchblob/main/LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.
