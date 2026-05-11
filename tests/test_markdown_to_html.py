from textwrap import dedent
import unittest

from htmlnode import HTMLNode, LeafNode
from markdown_to_html import markdown_to_textnodes, markdown_to_html_node
from textnode import TextNode, TextType


class TestsTextToTextNodes(unittest.TestCase):
    def test_general_case(self):

        markdown = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        template = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode(
                None,
                TextType.IMAGE,
                {
                    "alt": "obi wan image",
                    "src": "https://i.imgur.com/fJRm4Vk.jpeg",
                },
            ),
            TextNode(" and a ", TextType.PLAIN),
            TextNode(
                "link",
                TextType.LINK,
                {
                    "href": "https://boot.dev"
                },
            ),
        ]

        self.assertEqual(
            markdown_to_textnodes(markdown),
            template,
        )


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_single_line_of_text(self):
        markdown = "simple line of text"
        html = "<div><p>simple line of text</p></div>"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )

    def test_single_line_with_structure(self):
        markdown = "This is a **test case** with _structure_, an image (![image](www.example.com)) and a [link](www.example.com). Also some `code`."
        html = '<div><p>This is a <b>test case</b> with <i>structure</i>, an image (<img alt="image" src="www.example.com">) and a <a href="www.example.com">link</a>. Also some <code>code</code>.</p></div>'

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )

    def test_isolated_heading_top_level(self):
        markdown = "# Heading 1"
        html = "<div><h1>Heading 1</h1></div>"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )

    def test_isolated_heading_lower_level(self):
        markdown = "### Heading #3"
        html = "<div><h3>Heading #3</h3></div>"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )

    def test_isolated_code(self):
        markdown = "```\nint **x = 1; int **y = 2;```"
        html = "<div><pre><code>int **x = 1; int **y = 2;</code></pre></div>"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )

    def test_isolated_quote(self):
        markdown = dedent(
            """\
            > quote line one
            > quote line two
            > quote line three"""
        )

        html = "<div><blockquote>quote line one<br>quote line two<br>quote line three</blockquote></div>"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )

    def test_isolated_unordered_list(self):
        markdown = dedent(
            """\
            - Item 1
            - Item 2
            - Item 3"""
        )

        html = "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )

    def test_isolated_ordered_list(self):
        markdown = dedent(
            """\
            1. Item 1
            2. Item 2
            3. Item 3"""
        )

        html = "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )

    def test_several_blocks(self):
        self.maxDiff = None
        markdown = dedent(
            """\
            # heading #1

            ## heading #2

            A **markdown** file may contain several _blocks_.

            - item 1
            - item 2
            - item 3

            1. item 1
            2. item 2
            3. item 3

            > quote line 1
            > quote line 2
            > quote line 3

            ```
            int x = 1;
            ```

            One last paragraph."""
        )

        html = "<div><h1>heading #1</h1><h2>heading #2</h2><p>A <b>markdown</b> file may contain several <i>blocks</i>.</p><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul><ol><li>item 1</li><li>item 2</li><li>item 3</li></ol><blockquote>quote line 1<br>quote line 2<br>quote line 3</blockquote><pre><code>int x = 1;</code></pre><p>One last paragraph.</p></div>"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            html,
        )


if __name__ == "__main__":
    unittest.main()

