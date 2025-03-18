from textnode import TextNode, TextType

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