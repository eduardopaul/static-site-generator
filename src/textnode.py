from enum import Enum


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"
    IMAGE = "image"
    CODE = "code"


class TextNode:
    def __init__(self, text=None, text_type=TextType.PLAIN, props=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.props= props

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.props == other.props
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.props})"

