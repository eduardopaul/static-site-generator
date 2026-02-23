import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = HTMLNode(
                props={
                    "href": "https://www.google.com",
                    "target": "_blank",
                },
        ).props_to_html()

        props_template = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(props, props_template)

    def test_equality(self):
        htmlnode1 = HTMLNode(
            tag="p",
            value="Some text.",
        )

        htmlnode2 = HTMLNode(
            tag="p",
            value="Some text.",
        )

        self.assertEqual(htmlnode1, htmlnode2)


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

    def test_image_tag(self):
        leafnode = LeafNode(
            tag="img",
            value=None,
            props={"src": "img.jpg", "alt": "alt text"},
        )

        html = leafnode.to_html()

        template = '<img src="img.jpg" alt="alt text">'

        self.assertEqual(
            html,
            template,
        )

    def test_tag_with_props(self):
        node = LeafNode(
                tag="a",
                value="Click me!",
                props={"href": "https://www.google.com"},
        )
        template = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), template)


class TestParentNode(unittest.TestCase):
    def test_single_leaf_child(self):
        leaf_node = LeafNode(
            tag="b",
            value="Test stuff.",
        )

        parent_node = ParentNode(
            tag="p",
            children=[leaf_node],
        )

        template = '<p><b>Test stuff.</b></p>'

        self.assertEqual(parent_node.to_html(), template)

    def test_multiple_leaf_children(self):
        leaf_node1 = LeafNode(
            tag="b",
            value="Test bold.",
        )

        leaf_node2 = LeafNode(
            tag="i",
            value="Test italic.",
        )

        parent_node = ParentNode(
            tag="p",
            children=[leaf_node1, leaf_node2],
        )

        template = '<p><b>Test bold.</b><i>Test italic.</i></p>'

        self.assertEqual(parent_node.to_html(), template)

    def test_multilevel(self):
        leaf_node1 = LeafNode(
            tag="b",
            value="Test bold.",
        )

        leaf_node2 = LeafNode(
            tag="i",
            value="Test italic.",
        )

        subparent_node = ParentNode(
            tag="span",
            children=[leaf_node1, leaf_node2],
        )

        parent_node = ParentNode(
            tag="p",
            children=[subparent_node],
        )

        template = '<p><span><b>Test bold.</b><i>Test italic.</i></span></p>'

        self.assertEqual(parent_node.to_html(), template)

    def test_with_props(self):
        leaf_node = LeafNode(
            tag="a",
            value="link",
            props={"href": "https://www.example.com/index.html"}
        )

        parent_node = ParentNode(
            tag="div",
            children=[leaf_node],
            props={"class": "test_class"},
        )

        template = '<div class="test_class"><a href="https://www.example.com/index.html">link</a></div>'

        self.assertEqual(parent_node.to_html(), template)

    def test_with_nonleaf_content(self):
        leaf_node_bold = LeafNode(
            tag="b",
            value="Bold text.",
        )

        leaf_node_normal = LeafNode(
            tag=None,
            value=" Normal text.",
        )

        parent_node = ParentNode(
            tag="p",
            children=[leaf_node_bold, leaf_node_normal],
        )

        template = '<p><b>Bold text.</b> Normal text.</p>'

        self.assertEqual(parent_node.to_html(), template)


if __name__ == "__main__":
    unittest.main()

