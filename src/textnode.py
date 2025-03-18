from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        if self.url is None:
            return f"TextNode(\"{self.text}\", {self.text_type})" 
        return f"TextNode(\"{self.text}\", {self.text_type}, \"{self.url}\")"


def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            case _:
                raise Exception("Invalid text type")
            
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            text = node.text
            while delimiter in text:
                fst_index = text.find(delimiter)
                snd_index = text.find(delimiter, fst_index + len(delimiter))

                if snd_index == -1:
                    raise ValueError("Invalid Markdown: No trailing delimiter!")
                nodes.append(TextNode(text[:fst_index], TextType.TEXT))
                nodes.append(TextNode(text[fst_index+1:snd_index], text_type))
                remaining_text = text[snd_index+1:]
                text = remaining_text
            
            if text:
                nodes.append(TextNode(text, TextType.TEXT))

    return nodes