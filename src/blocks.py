from enum import Enum
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
