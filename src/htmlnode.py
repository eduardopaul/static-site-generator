class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if (self.props is None) or (isinstance(self.props, dict) and len(self.props) == 0):
            return ""

        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'

        return result

    def __repr__(self):
        print(f"HTMLNode\ntag: {tag}\nvalue: {value}\nchildren: {children}\nprops: {props}\n")


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("A LeafNode has to have a value.")
        
        if self.tag is None:
            resulting_html = self.value
        else:
            opening_tag = f"<{self.tag}" + self.props_to_html() + ">" if self.props else f"<{self.tag}>"
            closing_tag = f"</{self.tag}>"
            resulting_html = opening_tag + self.value + closing_tag

        return resulting_html

    def __repr__(self):
        print(f"HTMLNode\ntag: {tag}\nvalue: {value}\nprops: {props}\n")


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A ParentNode has to have a tag.")

        if not self.children:
            raise ValueError("It is mandatory that a ParentNode has associated children.")

        parent_opening_tag = f"<{self.tag}" + self.props_to_html() + ">" if self.props else f"<{self.tag}>"
        parent_closing_tag = f'</{self.tag}>'

        parent_content = "".join(
            child.to_html()
            for child in self.children
        )

        resulting_html = parent_opening_tag + parent_content + parent_closing_tag

        return resulting_html

