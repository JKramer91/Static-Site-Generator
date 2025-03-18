import re
from textnode import TextNode, TextType
from functools import partial

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
                nodes.append(TextNode(text[fst_index+len(delimiter):snd_index], text_type))
                remaining_text = text[snd_index+len(delimiter):]
                text = remaining_text
            
            if text:
                nodes.append(TextNode(text, TextType.TEXT))

    return nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        
        links = extract_markdown_images(node.text)
        if not links:
            nodes.append(node)
            continue
        remaining_text = node.text
        for text, url in links:
            sections = remaining_text.split(f"![{text}]({url})", 1)
            nodes.append(TextNode(sections[0], TextType.TEXT))
            nodes.append(TextNode(text, TextType.IMAGE, url))
            remaining_text = sections[1]
        
        if remaining_text:
            nodes.append(TextNode(remaining_text, TextType.TEXT))

    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        
        links = extract_markdown_links(node.text)
        if not links:
            nodes.append(node)
            continue
        remaining_text = node.text
        for text, url in links:
            sections = remaining_text.split(f"[{text}]({url})", 1)
            nodes.append(TextNode(sections[0], TextType.TEXT))
            nodes.append(TextNode(text, TextType.LINK, url))
            remaining_text = sections[1]
        
        if remaining_text:
            nodes.append(TextNode(remaining_text, TextType.TEXT))

    return nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes