import unittest

from htmlnode import LeafNode
from markdown_to_html import markdown_to_textnodes, textnodes_to_leafnodes
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


class TestTextnodesToLeafnodes(unittest.TestCase):
    def test_leaves_with_simple_delimiters(self):
        textnodes = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word. We also have a small ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, {"href": "example.com"}),
            TextNode(None, TextType.IMAGE, {"alt": "alt text", "src": "image.png"}),

        ]

        template = [
            LeafNode(value="This is text with an ", tag=None),
            LeafNode(value="italic", tag="i"),
            LeafNode(value=" and a ", tag=None),
            LeafNode(value="bold", tag="b"),
            LeafNode(value=" word. We also have a small ", tag=None),
            LeafNode(value="code block", tag="code"),
            LeafNode(value=" and a ", tag=None),
            LeafNode(value="link", tag="a", props={"href": "example.com"}),
            LeafNode(value=None, tag="img", props={"alt": "alt text", "src": "image.png"}),
        ]

        leafnodes = textnodes_to_leafnodes(textnodes)

        self.assertListEqual(
                leafnodes,
                template,
        )


if __name__ == "__main__":
    unittest.main()

