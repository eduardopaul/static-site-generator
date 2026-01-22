from htmlnode import LeafNode
import markdown_functions
from markdown_block_functions import markdown_to_blocks, block_to_block_type
from textnode import TextNode, TextType


def markdown_to_textnodes(markdown):
    input_textnode = TextNode(markdown, TextType.PLAIN)
    textnodes =  markdown_functions.split_nodes_delimiter([input_textnode], "**", TextType.BOLD)
    textnodes = markdown_functions.split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = markdown_functions.split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = markdown_functions.split_nodes_image(textnodes)
    textnodes = markdown_functions.split_nodes_link(textnodes)

    return textnodes


def textnodes_to_leafnodes(textnodes):
    leafnodes = []
    for textnode in textnodes:
        text = textnode.text
        tag = get_tag_from_texttype(textnode.text_type)

        leafnodes.append(
            LeafNode(
                tag=tag,
                value=text,
            )
        )

    return leafnodes


def get_tag_from_texttype(texttype):
    match texttype:
        case TextType.PLAIN:
            tag = None
        case TextType.ITALIC:
            tag = 'i'
        case TextType.BOLD:
            tag = 'b'

    return tag


