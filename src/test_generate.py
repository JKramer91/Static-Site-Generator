import unittest
from generate import extract_title

class TestExtractTitle(unittest.TestCase):
       
    def test_extract_title_valid(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")
    
    def test_extract_title_invalid(self):
        md = "## Hello"
        with self.assertRaises(Exception):
            extract_title(md)