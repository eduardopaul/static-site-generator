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
    def __init__(self):
        self.parentNode = None
        self.parentElement = None

        self.childNodes = []
        self.firstChild = None
        self.lastChild = None

        self.previousSibling = None
        self.nextSibling = None

    def _update_first_and_last_children(self):
        if self.childNodes:
            self.firstChild = self.childNodes[0]
            self.lastChild = self.childNodes[-1]
        else:
            self.firstChild = None
            self.lastChild = None

    def _set_parentNode(self, parentNode):
        self.parentNode = parentNode

        if isinstance(parentNode, Element):
            self.parentElement = parentNode

        idx = parentNode.childNodes.index(self)
        if idx > 0:
            self.previousSibling = parentNode.childNodes[idx-1]
        if idx < len(parentNode.childNodes) - 1:
            self.nextSibling = parentNode.childNodes[idx+1]

    def _unset_parentNode(self):
        self.parentNode = None
        self.parentElement = None
        self.previousSibling = None
        self.nextSibling = None

    def appendChild(self, childNode):
        if not isinstance(childNode, Node):
            raise TypeError(f"The parameter `childNode` must be a `Node`, not `{type(childNode).__name__}`")

        if childNode.parentNode is not None:
            childNode.parentNode.removeChild(childNode)

        self.childNodes.append(childNode)
        childNode._set_parentNode(self)
        self._update_first_and_last_children()

    def removeChild(self, childNode):
        if not isinstance(childNode, Node):
            raise TypeError(f"The parameter `childNode` must be a `Node`, not `{type(childNode).__name__}`")

        if childNode not in self.childNodes:
            return

        self.childNodes.remove(childNode)
        childNode._unset_parentNode()
        self._update_first_and_last_children()

    def insertBefore(self, newChildNode, referenceChildNode):
        if not isinstance(newChildNode, Node):
            raise TypeError(f"The parameter `newChildNode` must be a `Node`, not `{type(newChildNode).__name__}`")

        if not isinstance(referenceChildNode, Node):
            raise TypeError(f"The parameter `referenceChildNode` must be a `Node`, not `{type(referenceChildNode).__name__}`")

        if referenceChildNode not in self.childNodes:
            raise ValueError("The given `referenceChildNode` is not one of current the `Node`'s children.")

        if newChildNode.parentNode is not None:
            newChildNode.parentNode.removeChild(newChildNode)

        idx = self.childNodes.index(referenceChildNode)
        self.childNodes.insert(idx, newChildNode)
        self._update_first_and_last_children()

        newChildNode._set_parentNode(self)

    def replaceChild(self, newChildNode, oldChildNode):
        if not isinstance(newChildNode, Node):
            raise TypeError(f"The parameter `newChildNode` must be a `Node`, not `{type(newChildNode).__name__}`")

        if not isinstance(oldChildNode, Node):
            raise TypeError(f"The parameter `oldChildNode` must be a `Node`, not `{type(oldChildNode).__name__}`")

        if oldChildNode not in self.childNodes:
            raise ValueError("The given `oldChildNode` is not one of current the `Node`'s children.")

        idx = self.childNodes.index(oldChildNode)
        self.childNodes[idx] = newChildNode
        self._update_first_and_last_children()

        newChildNode._set_parentNode(self)
        oldChildNode._unset_parentNode()


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

