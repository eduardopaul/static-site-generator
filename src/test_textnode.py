import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_node1 = TextNode("This is some test text.", TextType.BOLD)
        text_node2 = TextNode("This is some test text.", TextType.BOLD)
        self.assertEqual(text_node1, text_node2)

    def test_full_eq(self):
        text_node1 = TextNode("This is some test text.", TextType.BOLD, url="www.example.com")
        text_node2 = TextNode("This is some test text.", TextType.BOLD, url="www.example.com")
        self.assertEqual(text_node1, text_node2)

    def test_diff_url(self):
        text_node1 = TextNode("This is some test text.", TextType.BOLD, url="www.example.com/page1")
        text_node2 = TextNode("This is some test text.", TextType.BOLD, url="www.example.com/page2")
        self.assertNotEqual(text_node1, text_node2)

    def test_url_none(self):
        text_node1 = TextNode("This is some test text.", TextType.BOLD, url=None)
        text_node2 = TextNode("This is some test text.", TextType.BOLD, url=None)
        self.assertEqual(text_node1, text_node2)


if __name__ == "__main__":
    unittest.main()

