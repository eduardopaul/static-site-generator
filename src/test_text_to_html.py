import unittest

from text_to_html import text_node_to_html_node
from textnode import TextNode, TextType


class TextToHTMLTest(unittest.TestCase):
    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Some bold example text", "bold")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Some bold example text")

    def test_italic(self):
        node = TextNode("Some italic example text", "italic")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Some italic example text")

    def test_link(self):
        node = TextNode("link text", "link", props={"href": "example.com"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link text")
        self.assertEqual(html_node.props, {"href": "example.com"})

    def test_image(self):
        node = TextNode(None, "image", props={"alt": "alt text", "src": "images/img.png"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "images/img.png", "alt": "alt text"})

    def test_code(self):
        node = TextNode("for file in *; do echo '$file'; done", "code")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "for file in *; do echo '$file'; done")

if __name__ == "__main__":
    unittest.main()

