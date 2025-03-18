from enum import Enum
from htmlnode import HTMLNode
from inline import text_to_textnodes
from textnode import text_node_to_html_node
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    cleaned_lines = filter(str.strip, block_strings)
    stripped_lines = list(map(str.strip, cleaned_lines))
    return stripped_lines

def is_valid_ordered_list(text):
    lines = text.strip().split('\n')
    for i, line in enumerate(lines, start=1):
        if not re.match(rf'^{i}\. ', line):
            return False
    return True

def block_to_block_type(block):
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    if re.match(r'^```.*```$', block, re.DOTALL):
        return BlockType.CODE
    if re.fullmatch(r'(>.*\n?)+', block):
        return BlockType.QUOTE
    if re.fullmatch(r'(- .*\n?)+', block):
        return BlockType.UNORDERED_LIST
    if is_valid_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def block_to_html_children(block, prefix_length, child_tag):
    children = []
    lines = block.split("\n")
    for line in lines:
        if len(line) > prefix_length: 
            value = line[prefix_length:].strip()
            if value: 
                inline_nodes = text_to_children(value)
                children.append(inline_nodes)
    return children

def block_to_html_node(block):
    match block:
        case BlockType.PARAGRAPH:
            return 1
        case BlockType.HEADING:
            return 1
        case BlockType.CODE:
            return 1
        case BlockType.QUOTE:
            children = block_to_html_children(block, 1, "p")
            return HTMLNode("blockquote", None, children)
        case BlockType.UNORDERED_LIST:
            children = block_to_html_children(block, 2, "li")
            return HTMLNode("ul", None, children)
        case BlockType.ORDERED_LIST:
            children = block_to_html_children(block, 3, "li")
            return HTMLNode("ol", None, children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
    

if __name__ == "__main__":
    test = """- This is a line\n- This is another line\n- This is the last line"""
    print(text_to_children(test))