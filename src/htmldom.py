from enum import Enum


class Tag(Enum):
    A = "a"
    BODY = "body"
    DIV = "div"
    HEAD = "head"
    HTML = "html"
    IMG = "img"
    P = "p"
    STRONG = "strong"


class Node:
    pass


class ElementNode(Node):
    def __init__(self, tag, attr=None):
        if not (attr is None or isinstance(attr, dict)):
            raise TypeError("Parameter `attr` should be of type `None` or `dict`.")

        self.tag = Tag(tag)
        self.attr = attr
        self.children = []
        self._self_closing = self._is_self_closing()

    def _is_self_closing(self):
        self_closing_tags = [Tag.IMG]
        return self.tag in self_closing_tags

    def append_child(self, child):
        self.children.append(child)

    def _format_attr(self):
        if self.attr is None:
            return ""

        return "".join(
            f' {key}="{value}"'
            for key, value in self.attr.items()
        )

    def to_html(self):
        opening_tag = f"<{self.tag.value}{self._format_attr()}>"

        html_string = opening_tag

        if not self._self_closing:
            content = "".join(child.to_html() for child in self.children)
            closing_tag = f"</{self.tag.value}>"
            html_string += content + closing_tag

        return html_string


class TextNode(Node):
    def __init__(self, text):
        self.text = text

    def to_html(self):
        return self.text

