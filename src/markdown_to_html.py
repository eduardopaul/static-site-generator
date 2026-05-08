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
        props = textnode.props

        leafnodes.append(
            LeafNode(
                tag=tag,
                value=text,
                props=props,
            )
        )

    return leafnodes


def get_tag_from_texttype(texttype):
    match texttype:
        case TextType.PLAIN:
            tag = None
        case TextType.BOLD:
            tag = 'b'
        case TextType.ITALIC:
            tag = 'i'
        case TextType.CODE:
            tag = 'code'
        case TextType.LINK:
            tag = 'a'
        case TextType.IMAGE:
            tag = 'img'

    return tag


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """Consume a markdown page and produce from it its equivalent as an HTMLNode ready to be displayed as a web page."""
    return HTMLNode()

