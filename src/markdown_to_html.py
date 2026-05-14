from re import findall, match, split, sub, MULTILINE

from htmlnode import HTMLNode
from markdown_block_functions import BlockType, block_to_block_type
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

    list_of_blocks = split(r"\n\n+", markdown)
    for block_markdown in list_of_blocks:
        block_type = block_to_block_type(block_markdown)

        match block_type:
            case BlockType.PARAGRAPH:
                paragraph_node = HTMLNode(tag="p", children=[])

                block_markdown = sub("\n", " ", block_markdown)

                textnodes = markdown_to_textnodes(block_markdown)
                for textnode in textnodes:
                    paragraph_node.children.append(
                        text_node_to_html_node(textnode)
                    )

                html_node.children.append(paragraph_node)

            case BlockType.HEADING:
                prefix = match(r"\s*#+ ", block_markdown).group(0)
                heading_level = len(findall("#", prefix))

                html_node.children.append(
                    HTMLNode(
                        tag=f"h{heading_level}",
                        value=sub("#+ ", "", block_markdown).strip(),
                    )
                )

            case BlockType.CODE:
                block_markdown = sub("```\n", "", block_markdown)
                block_markdown = sub("\n*```", "", block_markdown)

                html_node.children.append(
                    HTMLNode(
                        tag="pre",
                        children=[
                            HTMLNode(
                                tag="code",
                                value=block_markdown,
                            ),
                        ]
                    )
                )

            case BlockType.QUOTE:
                block_markdown = sub("^> *", "", block_markdown, flags=MULTILINE)
                block_markdown = sub("\n", "<br>", block_markdown)

                html_node.children.append(
                    HTMLNode(
                        tag="blockquote",
                        value=block_markdown,
                    )
                )

            case BlockType.UNORDERED_LIST:
                block_markdown = sub("^- ", "", block_markdown, flags=MULTILINE)
                block_markdown = block_markdown.splitlines()

                html_lines = []
                for line in block_markdown:
                    html_lines.append("<li>" + line + "</li>")

                block_markdown = "".join(html_lines)

                html_node.children.append(
                    HTMLNode(
                        tag="ul",
                        value=block_markdown,
                    )
                )

            case BlockType.ORDERED_LIST:
                block_markdown = sub(r"^\d+\. ", "", block_markdown, flags=MULTILINE)
                block_markdown = block_markdown.splitlines()

                html_lines = []
                for line in block_markdown:
                    html_lines.append("<li>" + line + "</li>")

                block_markdown = "".join(html_lines)

                html_node.children.append(
                    HTMLNode(
                        tag="ol",
                        value=block_markdown,
                    )
                )


    return html_node

