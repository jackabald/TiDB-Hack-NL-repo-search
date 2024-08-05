import unittest
from unittest.mock import patch, MagicMock
import json
import numpy as np
from src.code_search import generate_query_vector, retrieve_code_vectors, search_code_snippets

# Mocking the environment for tests
@patch("src.code_search.connection")
@patch("src.code_search.model")
@patch("src.code_search.tokenizer")
class TestCodeSearch(unittest.TestCase):

    def test_generate_query_vector(self, mock_tokenizer, mock_model, mock_connection):
        # Mocking the tokenizer and model behavior
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        # Mock the model output
        mock_outputs = MagicMock()
        mock_outputs.last_hidden_state = MagicMock()
        mock_outputs.last_hidden_state.mean.return_value = np.random.rand(1, 768)
        mock_model.return_value = mock_outputs

        # Test the function
        query = "function that initializes a binary search tree"
        vector = generate_query_vector(query)

        # Assertions
        self.assertEqual(vector.shape, (768,))  # Assuming 768 is the hidden size of the model

    def test_retrieve_code_vectors(self, mock_connection, mock_tokenizer, mock_model):
        # Mocking the database response
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            ("file_path.py", "foo", "FunctionDef", 1, 5, "def foo(): pass", json.dumps([0.1, 0.2, 0.3]))
        ]

        # Test the function
        snippets = retrieve_code_vectors()

        # Assertions
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0]["function_name"], "foo")
        self.assertEqual(snippets[0]["vector"].tolist(), [0.1, 0.2, 0.3])

    def test_search_code_snippets(self, mock_connection, mock_tokenizer, mock_model):
        # Mocking the database response for the search
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            ("file_path.py", "foo", "FunctionDef", 1, 5, "def foo(): pass", 0.9)
        ]

        # Mocking the query vector
        query_vector = np.array([0.1, 0.2, 0.3])

        # Test the function
        results = search_code_snippets(query_vector)

        # Assertions
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["function_name"], "foo")
        self.assertAlmostEqual(results[0]["similarity"], 0.9, places=2)

if __name__ == '__main__':
    unittest.main()
