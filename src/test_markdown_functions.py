import unittest

from textnode import TextNode, TextType
from markdown_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image


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


class TestSplitNodesLink(unittest.TestCase):
    def test_simple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )

        template = [
            TextNode(
                "This is text with a link ",
                TextType.PLAIN,
            ),
            TextNode(
                "to boot dev",
                TextType.LINK,
                "https://www.boot.dev",
            ),
            TextNode(
                " and ",
                TextType.PLAIN,
            ),
            TextNode(
                "to youtube",
                TextType.LINK,
                "https://www.youtube.com/@bootdotdev",
            ),
        ]

        self.assertEqual(
            split_nodes_link(
                old_nodes=[node]
            ),
            template,
        )

    def test_no_links(self):
        node = TextNode(
            "Some random markdown text with no links.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])

        template = [
            TextNode(
                "Some random markdown text with no links.",
                TextType.PLAIN,
            )
        ]

        self.assertListEqual(
            new_nodes,
            template,
        )

    def test_link_and_image(self):
        node = TextNode(
                "Some text with an ![image](https://www.example.com/image.png) and a [link](https://www.example.com/link.html)",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_link([node])

        template = [
            TextNode(
                "Some text with an ![image](https://www.example.com/image.png) and a ",
                TextType.PLAIN,
            ),
            TextNode(
                "link",
                TextType.LINK,
                "https://www.example.com/link.html",
            ),
        ]

        self.assertListEqual(
            new_nodes,
            template,
        )

    def test_multiple_input_nodes_with_different_types(self):
        nodes = [
            TextNode(
                "Text with a ",
                TextType.PLAIN,
            ),
            TextNode(
                "bold",
                TextType.BOLD,
            ),
            TextNode(
                " part and a [link](https://www.example.com/)",
                TextType.PLAIN,
            ),
        ]

        new_nodes = split_nodes_link(nodes)

        template = [
            TextNode(
                "Text with a ",
                TextType.PLAIN,
            ),
            TextNode(
                "bold",
                TextType.BOLD,
            ),
            TextNode(
                " part and a ",
                TextType.PLAIN,
            ),
            TextNode(
                "link",
                TextType.LINK,
                "https://www.example.com/",
            ),
        ]

        self.assertListEqual(
            new_nodes,
            template,
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode(
          "Some random markdown text with no images.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])

        template = [
            TextNode(
                "Some random markdown text with no images.",
                TextType.PLAIN,
            )
        ]

        self.assertListEqual(
            new_nodes,
            template,
        )

    def test_link_and_image(self):
        node = TextNode(
                "Some text with an ![image](https://www.example.com/image.png) and a [link](https://www.example.com/link.html)",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_image([node])

        template = [
            TextNode(
                "Some text with an ",
                TextType.PLAIN,
            ),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://www.example.com/image.png"
            ),
            TextNode(
                " and a [link](https://www.example.com/link.html)",
                TextType.PLAIN,
            ),
        ]

        self.assertListEqual(
            new_nodes,
            template,
        )

class TestsTextToTextNodes(unittest.TestCase):
    def test_general_case(self):
        from markdown_functions import text_to_textnodes

        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        template = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(
            text_to_textnodes(text),
            template,
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_simple_case(self):
        from markdown_block_functions import markdown_to_blocks
        from textwrap import dedent

        md = dedent("""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """)

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()

