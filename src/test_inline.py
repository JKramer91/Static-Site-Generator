import unittest
from textnode import TextNode, TextType
from inline import split_nodes_delimiter
class TestInline(unittest.TestCase):

    def test_one_inlines(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        cmp = [TextNode("This is a text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), cmp)

    def test_two_inlines(self):
        node = TextNode("This is a text with a `code block` word and another `code block`", TextType.TEXT)
        cmp = [TextNode("This is a text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word and another ", TextType.TEXT), TextNode("code block", TextType.CODE)]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), cmp)

    def test_inline_bold(self):
        node = TextNode("This is a text with a **bold block** word", TextType.TEXT)
        cmp = [TextNode("This is a text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), cmp)
