import unittest
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from src.utils.utils import read_json_file, get_completion_from_messages, parse_string_to_json


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_read_json_file(self):
        file_path = './src/data/orders.json'
        json_file = read_json_file(file_path)
        self.assertIsInstance(json_file, dict)

    def test_get_completion_from_messages(self):
        delimiter ='###'
        system_message = f"""
        You will be provided with customer service queries. \
        The customer service query will be delimited with \
        {delimiter} characters.
        Classify each query into a category. \
        Provide your output in json format with the \
        keys: category.
        categories: Products, Orders, \
        Return Policies.
        """
        messages = [
            {'role': 'system',
             'content': system_message},
            {'role': 'user',
             'content': f"{delimiter}hello{delimiter}"},
        ]

        response = get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500)
        self.assertEqual(response, '{\n  "category": "Uncategorized"\n}')

    def test_parse_string_to_json(self):
        text = "{'role': 'system', 'content': 'you are a chatbot'}"
        jsonstring = parse_string_to_json(text)
        self.assertEqual(jsonstring, {"content": "you are a chatbot", "role": "system"})