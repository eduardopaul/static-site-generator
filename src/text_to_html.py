from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("The input should be a TextNode instance.")

    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(
                tag=None,
                value=text_node.text,
            )
        case TextType.BOLD:
            return LeafNode(
                tag="b",
                value=text_node.text,
            )
        case TextType.ITALIC:
            return LeafNode(
                tag="i",
                value=text_node.text,
            )
        case TextType.LINK:
            return LeafNode(
                tag="a",
                value=text_node.text,
                props=text_node.props,
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value=None,
                props=text_node.props,
            )
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case _:
            raise TypeError("TextNode's text_type should be one of PLAIN, BOLD, ITALIC, LINK, IMAGE or CODE")

