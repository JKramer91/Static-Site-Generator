from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
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
    children = []
    for node in text_nodes:
        child = text_node_to_html_node(node)
        children.append(child)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)
    
def heading_to_html_node(block):
    lvl = 0
    for char in block:
        if char == "#":
            lvl += 1
        else:
            break
    if lvl + 1 >= len(block):
        raise ValueError(f"Invalid heading: needs text after hash symbols")
    text = block[lvl+1:]
    children = text_to_children(text)
    return ParentNode(f"h{lvl}", children)

def code_to_html_node(block):
    text = block[3:-3]
    text_node = TextNode(text, TextType.CODE)
    code_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_line = (line[1:].strip())
        new_lines.append(new_line)
    child = " ".join(new_lines)
    children = text_to_children(child)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        child = text_to_children(line[2:])
        children.append(ParentNode("li", child))
    return ParentNode("ul", children)

def olist_to_html_node(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        child = text_to_children(line[3:])
        children.append(ParentNode("li", child))
    return ParentNode("ol", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
        case _:
            raise ValueError("Invalid block type!")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        child = block_to_html_node(block)
        children.append(child)
    return ParentNode("div", children)
