import unittest
from unittest.mock import MagicMock, patch
import os
from src.code_search import generate_query_vector

class TestGenerateQueryVector(unittest.TestCase):
    def test_generate_query_vector(self):
        # Simulate a query
        query = "What file is the function foo defined in?"
        
        # Call the generate vector function
        vector = generate_query_vector(query)
        
        # Assertions
        self.assertEqual(len(vector), 768)  # Typical vector size for BERT models


if __name__ == '__main__':
    unittest.main()