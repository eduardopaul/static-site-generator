import unittest

from textnode import TextNode, TextType
from markdown_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.PLAIN,
        )

        template = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(
            split_nodes_delimiter(
                old_nodes=[node],
                delimiter="`",
                text_type=TextType.CODE,
            ),
            template,
        )

    def test_italic(self):
        node = TextNode(
            "This is text with an _italic_ word",
            TextType.PLAIN,
        )

        template = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(
            split_nodes_delimiter(
                old_nodes=[node],
                delimiter="_",
                text_type=TextType.ITALIC,
            ),
            template,
        )

    def test_bold(self):
        node = TextNode(
            "This is text with a **bold** word",
            TextType.PLAIN,
        )

        template = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(
            split_nodes_delimiter(
                old_nodes=[node],
                delimiter="**",
                text_type=TextType.BOLD,
            ),
            template,
        )

    def test_non_plain_node(self):
        node = TextNode(
            "This text is not PLAIN.",
            TextType.BOLD,
        )

        template = [
            TextNode(
                "This text is not PLAIN.",
                TextType.BOLD,
            )
        ]

        self.assertEqual(
            split_nodes_delimiter(
                old_nodes=[node],
                delimiter="**",
                text_type=TextType.BOLD,
            ),
            template,
        )

    def test_multiple_children_nodes(self):
        node = TextNode(
            "This node contains _italic_ and **bold** parts.",
            TextType.PLAIN,
        )

        template = [
            TextNode(
                "This node contains _italic_ and ",
                TextType.PLAIN,
            ),
            TextNode(
                "bold",
                TextType.BOLD,
            ),
            TextNode(
                " parts.",
                TextType.PLAIN,
            ),
        ]

        self.assertEqual(
            split_nodes_delimiter(
                old_nodes=[node],
                delimiter="**",
                text_type=TextType.BOLD,
            ),
            template,
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode(
                "This node contains _italic_ and ",
                TextType.PLAIN,
            ),
            TextNode(
                "bold",
                TextType.BOLD,
            ),
            TextNode(
                " parts.",
                TextType.PLAIN,
            )
        ]

        template = [
            TextNode(
                "This node contains ",
                TextType.PLAIN,
            ),
            TextNode(
                "italic",
                TextType.ITALIC,
            ),
            TextNode(
                " and ",
                TextType.PLAIN,
            ),
            TextNode(
                "bold",
                TextType.BOLD,
            ),
            TextNode(
                " parts.",
                TextType.PLAIN,
            )
        ]

        self.assertEqual(
            split_nodes_delimiter(
                old_nodes=nodes,
                delimiter="_",
                text_type=TextType.ITALIC,
            ),
            template,
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        template = [("image", "https://i.imgur.com/zjjcJKZ.png")]

        self.assertListEqual(matches, template)

    def test_multiple_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and another ![one](https://blabla.com)"
        )

        template = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("one", "https://blabla.com"),
        ]

        self.assertListEqual(matches, template)

    def test_with_link(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and a [link](https://blabla.com)"
        )

        template = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
        ]

        self.assertListEqual(matches, template)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )

        template = [("link", "https://i.imgur.com/zjjcJKZ.png")]

        self.assertListEqual(matches, template)

    def test_several_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )

        template = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertListEqual(matches, template)

    def test_with_image(self):
        matches = extract_markdown_links(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and a [link](https://blabla.com)"
        )

        template = [
            ("link", "https://blabla.com"),
        ]

        self.assertListEqual(matches, template)

    def test_with_image_reverse(self):
        matches = extract_markdown_links(
                "This is text with a [link](https://blabla.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)."
        )

        template = [
            ("link", "https://blabla.com"),
        ]

        self.assertListEqual(matches, template)


if __name__ == "__main__":
    unittest.main()

