import unittest
from textnode import TextNode, TextType
from inline import split_nodes_delimiter
class TestInline(unittest.TestCase):

    def test_one_inlines(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        cmp = [TextNode("This is a text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), cmp)