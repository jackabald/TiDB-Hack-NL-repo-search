import os

from index_code import extract_code_snippets

# TODO use gen-ai if needed and sql query
def search_code(codebase_path):
    results = []
    
    # Iterate through all files in the codebase
    for root, files in os.walk(codebase_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Extract code snippets from the file
            snippets = extract_code_snippets(file_path)
            
            # Add the file path and relevant information to the results
            result = {
                'file_path': file_path,
                'snippet': snippets,
                'explanation': 'This is a relevant code snippet for the query.'
            }
            results.append(result)
    return results
