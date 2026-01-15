import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()
