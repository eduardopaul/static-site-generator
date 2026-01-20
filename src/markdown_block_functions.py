
def markdown_to_blocks(markdown):
    list_of_blocks = markdown.split("\n\n")
    new_markdown = [
        block.strip()
        for block in list_of_blocks
    ]

    return new_markdown

