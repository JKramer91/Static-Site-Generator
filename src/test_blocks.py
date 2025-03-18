import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
        )

    def test_block_to_block_type_heading(self):
        block = "#### This is a heading block"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_block_type_code(self):
        block = "````This is a code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = ">This is a quote\n>This is a new line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_to_block_type_ulist(self):
        block = "- This is the first line\n- This is the second\n- This is the third"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_olist(self):
        block = "1. This is the first line\n2. This is the second\n3. This is the third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_paragraph(self):
        block = "This is a normal paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)