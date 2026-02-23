import unittest

import htmldom


class TestElementNode(unittest.TestCase):
    def test_regular_tag(self):
        node_html = htmldom.ElementNode(tag="p").to_html()
        template_html = "<p></p>"

        self.assertEqual(template_html, node_html)

    def test_incorrect_tag(self):
        with self.assertRaises(ValueError):
            node = htmldom.ElementNode(tag="d")

    def test_self_closing_tag(self):
        node_html = htmldom.ElementNode(tag="img").to_html()
        template_html = "<img>"

        self.assertEqual(template_html, node_html)

    def test_element_with_child(self):
        node = htmldom.ElementNode(tag="div")
        child_node = htmldom.ElementNode(tag="p")
        node.append_child(child_node)

        template_html = "<div><p></p></div>"

        self.assertEqual(template_html, node.to_html())

    def test_element_with_text_content(self):
        node = htmldom.ElementNode(tag="p")
        text_content = htmldom.TextNode(text="Text in the paragraph.")
        node.append_child(text_content)

        template_html = "<p>Text in the paragraph.</p>"

        self.assertEqual(template_html, node.to_html())

    def test_element_with_attributes(self):
        node = htmldom.ElementNode(tag="a", attr={"href": "example.com"})
        text_node = htmldom.TextNode(text="link")
        node.append_child(text_node)

        template_html = '<a href="example.com">link</a>'

        self.assertEqual(template_html, node.to_html())

    def test_incorrect_attr_type(self):
        with self.assertRaises(TypeError):
            node = htmldom.ElementNode(tag="a", attr=["href", "example.com"])

    def test_nested_elements(self):
        node_div = htmldom.ElementNode(tag="div")
        node_p_1 = htmldom.ElementNode(tag="p")
        node_text1 = htmldom.TextNode(text="This is a section with several paragraphs.")
        node_p_2 = htmldom.ElementNode(tag="p")
        node_text2 = htmldom.TextNode(text="Right here we have ")
        node_strong = htmldom.ElementNode(tag="strong")
        node_text3 = htmldom.TextNode(text="strong text")
        node_text4 = htmldom.TextNode(text=" and a ")
        node_link = htmldom.ElementNode(tag="a", attr={"href": "example.com"})
        node_text5 = htmldom.TextNode(text="link")
        node_text6 = htmldom.TextNode(text=".")

        node_div.append_child(node_p_1)
        node_p_1.append_child(node_text1)
        node_div.append_child(node_p_2)
        node_p_2.append_child(node_text2)
        node_p_2.append_child(node_strong)
        node_strong.append_child(node_text3)
        node_p_2.append_child(node_text4)
        node_p_2.append_child(node_link)
        node_link.append_child(node_text5)
        node_p_2.append_child(node_text6)

        node_p_3 = htmldom.ElementNode(tag="p")
        node_div.append_child(node_p_3)

        node_text7 = htmldom.TextNode(text="Here is also an image: ")
        node_p_3.append_child(node_text7)

        node_img = htmldom.ElementNode(tag="img", attr={"src": "img.jpg"})
        node_p_3.append_child(node_img)

        template_html = '<div><p>This is a section with several paragraphs.</p><p>Right here we have <strong>strong text</strong> and a <a href="example.com">link</a>.</p><p>Here is also an image: <img src="img.jpg"></p></div>'

        self.assertEqual(template_html, node_div.to_html())


if __name__ == "__main__":
    unittest.main()

