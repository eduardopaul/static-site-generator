import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_node1 = TextNode("This is some test text.", TextType.BOLD)
        text_node2 = TextNode("This is some test text.", TextType.BOLD)
        self.assertEqual(text_node1, text_node2)

    def test_full_eq(self):
        text_node1 = TextNode("This is some test text.", TextType.BOLD, props={"href": "one.html"})
        text_node2 = TextNode("This is some test text.", TextType.BOLD, props={"href": "one.html"})
        self.assertEqual(text_node1, text_node2)

    def test_diff_props(self):
        text_node1 = TextNode("This is some test text.", TextType.BOLD, props={"href": "one.html"})
        text_node2 = TextNode("This is some test text.", TextType.BOLD, props={"href": "two.html"})
        self.assertNotEqual(text_node1, text_node2)

    def test_props_none(self):
        text_node1 = TextNode("This is some test text.", TextType.BOLD, props=None)
        text_node2 = TextNode("This is some test text.", TextType.BOLD, props=None)
        self.assertEqual(text_node1, text_node2)


if __name__ == "__main__":
    unittest.main()

