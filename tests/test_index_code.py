import unittest
from unittest.mock import MagicMock, patch
import os
import textwrap
from src.index_code import extract_code_snippets, generate_graphcodebert_vector, store_in_tidb, index_code_directory

class TestCodeExtraction(unittest.TestCase):
    def test_extract_code_snippets(self):
        # Simulate a code file content
        code = textwrap.dedent("""
        def foo():
            pass

        class Bar:
            def __init__(self):
                self.x = 1
        """)
        
        # Write this code to a temporary filei
        with open("temp_test_file.py", "w") as f:
            f.write(code)
        
        # Call the function and check results
        snippets = extract_code_snippets("temp_test_file.py")
        
        # Assertions
        self.assertEqual(len(snippets), 3)
        self.assertEqual(snippets[0]['name'], 'foo')
        self.assertEqual(snippets[1]['name'], 'Bar')
        
        # Clean up
        os.remove("temp_test_file.py")

class TestEmbeddingGeneration(unittest.TestCase):
    def test_generate_graphcodebert_vector(self):
        # Simulate a code snippet
        code_snippet = "def foo(): return 42"
        
        # Call the generate vector function
        vector = generate_graphcodebert_vector(code_snippet)
        
        # Assertions
        self.assertEqual(len(vector), 768)  # Typical vector size for BERT models

class TestDatabaseStorage(unittest.TestCase):
    @patch('src.index_code.connection')
    def test_store_in_tidb(self, mock_connection):
        # Mock the cursor
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Example vectors data
        vectors = [{
            "name": "foo",
            "type": "FunctionDef",
            "vector": [0.1, 0.2, 0.3],  # TODO: replace with actual vector
            "start_line": 1,
            "end_line": 3,
            "code": "def foo(): return 42"
        }]
        
        # Call the store_in_tidb function
        store_in_tidb("fake_path.py", vectors)
        
        # Assertions
        mock_cursor.execute.assert_called_once()
        mock_connection.commit.assert_called_once()

class TestDirectoryIndexing(unittest.TestCase):
    @patch('src.index_code.extract_code_snippets')
    @patch('src.index_code.generate_vectors')
    @patch('src.index_code.store_in_tidb')
    def test_index_code_directory(self, mock_store, mock_generate, mock_extract):
        # Mocking the behaviors
        mock_extract.return_value = [{'name': 'foo', 'code': 'def foo(): pass'}]
        mock_generate.return_value = [{'vector': [0.1, 0.2, 0.3]}]
        
        # Create a fake directory structure
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('/fake_dir', ('subdir',), ('file1.py', 'file2.py'))
            ]
            
            # Call the function
            index_code_directory('/fake_dir')
            
            # Assertions
            self.assertTrue(mock_extract.called)
            self.assertTrue(mock_generate.called)
            self.assertTrue(mock_store.called)

if __name__ == '__main__':
    unittest.main()
