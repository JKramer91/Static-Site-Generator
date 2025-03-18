def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    cleaned_lines = filter(str.strip, block_strings)
    stripped_lines = list(map(str.strip, cleaned_lines))
    return stripped_lines
