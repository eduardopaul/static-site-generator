from enum import Enum
from re import match, search


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    list_of_blocks = markdown.split("\n\n")
    new_markdown = [
        block.strip()
        for block in list_of_blocks
    ]

    return new_markdown


def block_to_block_type(block):

    if match(r"#{1,6}", block):
        block_type = BlockType.HEADING
    elif match(r"```\n", block) and search(r"```$", block):
        block_type = BlockType.CODE
    elif all(match(r"> ", line) for line in block.splitlines()):
        block_type = BlockType.QUOTE
    elif all(match(r"- ", line) for line in block.splitlines()):
        block_type = BlockType.UNORDERED_LIST
    elif test_ordered_list(block):
        block_type = BlockType.ORDERED_LIST
    else:
        block_type = BlockType.PARAGRAPH

    return block_type


def test_ordered_list(block):
    try:
        first_idx = match(r"(\d+)\.", block).group(1)
    except AttributeError:
        return False

    idx = int(first_idx)

    lines = block.splitlines()
    for line in lines:
        if not match(f"{idx}\\.", line):
            return False
        idx += 1

    return True

