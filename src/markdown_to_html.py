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



#     text = "This is text with an _italic_ word."
#
# -> text_to_textnodes(text):
#     textnodes = [
#         TextNode("This is text with an ", TextType.PLAIN),
#         TextNode("italic", TextType.ITALIC),
#         TextNode(" word", TextType.PLAIN),
#     ]
#
# -> textnodes_to_leafnodes(textnodes):
#     leafnodes = [
#         LeafNode(value="This is text with an "),
#         LeafNode(value="italic", tag="i"),
#         LeafNode(value=" word"),
#     ]
#
# -> leafnodes_to_parentnode(leafnodes, blocktype):
#     parentnode = ParentNode(
#         tag=blocktype,
#         children=leafnodes,
#     )
#
# -> parentnode.to_html():
#     "<p>This is text with an <i>italic</i> word.</p>"


def markdown_to_html_node(markdown):
    pass


