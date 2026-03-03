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

        self.firstChild = None
        self.lastChild = None

        self.previousSibling = None
        self.nextSibling = None

    @property
    def childNodes(self):
        nodes = []
        node = self.firstChild

        while node:
            nodes.append(node)
            node = node.nextSibling

        return nodes

    def appendChild(self, childNode):
        if not isinstance(childNode, Node):
            raise TypeError(f"The parameter `childNode` should be a `Node`, but is a `{type(childNode).__name__}`.")

        if self.firstChild is None:
            self.firstChild = childNode
        else:
            self.lastChild.nextSibling = childNode
            childNode.previousSibling = self.lastChild

        self.lastChild = childNode
        childNode.parentNode = self

    def removeChild(self, childNode):
        if not isinstance(childNode, Node):
            raise TypeError(f"The parameter `childNode` should be a `Node`, but is a `{type(childNode).__name__}`.")

        if childNode in self.childNodes:
            if childNode is self.firstChild:
                if childNode is self.lastChild:
                    self.firstChild = None
                    self.lastChild = None
                else:
                    self.firstChild = childNode.nextSibling
                    self.firstChild.previousSibling = None

            elif childNode is self.lastChild:
                self.lastChild = childNode.previousSibling
                self.lastChild.nextSibling = None

            else:
                childNode.previousSibling.nextSibling = childNode.nextSibling
                childNode.nextSibling.previousSibling = childNode.previousSibling

            childNode.previousSibling = None
            childNode.nextSibling = None
            childNode.parentNode = None

    def insertBefore(self, newChildNode, referenceChildNode):
        if not isinstance(newChildNode, Node):
            raise TypeError(f"The parameter `newChildNode` should be a `Node`, but is a `{type(newChildNode).__name__}`")

        if not isinstance(referenceChildNode, Node):
            raise TypeError(f"The parameter `referenceChildNode` should be a `Node`, but is a `{type(referenceChildNode).__name__}`")

        if referenceChildNode not in self.childNodes:
            raise ValueError("The given `referenceChildNode` is not one of current the `Node`'s children.")

        if newChildNode.parentNode is not None:
            newChildNode.parentNode.removeChild(newChildNode)

        newChildNode.parentNode = self
        newChildNode.nextSibling = referenceChildNode
        newChildNode.previousSibling = referenceChildNode.previousSibling

        referenceChildNode.previousSibling = newChildNode
        newChildNode.previousSibling.nextSibling = newChildNode

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

