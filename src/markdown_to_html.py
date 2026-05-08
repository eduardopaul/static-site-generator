from htmlnode import HTMLNode
import markdown_functions
from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node


def markdown_to_textnodes(markdown):
    input_textnode = TextNode(markdown, TextType.PLAIN)
    textnodes = markdown_functions.split_nodes_delimiter([input_textnode], "**", TextType.BOLD)
    textnodes = markdown_functions.split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = markdown_functions.split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = markdown_functions.split_nodes_image(textnodes)
    textnodes = markdown_functions.split_nodes_link(textnodes)

    return textnodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """Consume a markdown document and produce from it a single `HTMLNode`. The output node should generate the expected html code, being a standalone `div` element."""

    html_node = HTMLNode(tag="div", children=[])

    textnodes = markdown_to_textnodes(markdown)
    for textnode in textnodes:
        html_node.children.append(
            text_node_to_html_node(textnode)
        )

    return html_node

