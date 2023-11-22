import unittest
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from src.controllers.rag import Rag


class TestRag(unittest.TestCase):

    def setUp(self) -> None:
        self.rag = Rag()

    def test_load_db(self):
        file = 'src/data/rag/docs/returns_policies/return_policies.pdf'
        chain_type = 'stuff'
        k = 4
        conversational_retrieval_chain = self.rag.load_db(file, chain_type, k)
        self.assertIsInstance(conversational_retrieval_chain, object)

    def test_query(self):
        query = 'could you let me know about the return policies?'
        rag_retrieval_history = []
        answer,  rag_retrieval_history = self.rag.query(query, rag_retrieval_history, debug=True)
        self.assertGreater(len(answer), 0)



