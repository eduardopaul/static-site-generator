import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_basic_tag(self):
        node = LeafNode(
            tag="p",
            value="Here is some test text.",
        )
        template = "<p>Here is some test text.</p>"
        self.assertEqual(node.to_html(), template)


    def test_empty_tag(self):
        node = LeafNode(tag="", value="")
        self.assertRaises(ValueError, node.to_html)


    def test_tag_with_props(self):
        node = LeafNode(
                tag="a",
                value="Click me!",
                props={"href": "https://www.google.com"},
        )
        template = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), template)


if __name__ == "__main__":
    unittest.main()
