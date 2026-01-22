from re import findall, fullmatch, match, split

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    Take an input list of nodes and split each one of them into new nodes marked by the given delimiter, such that the markdown gets structurally decomposed.
    '''
    new_nodes = []

    for node in old_nodes:
        split_node_text = node.text.split(delimiter)
        # even number of delimiters -> odd number of parts
        # even number of parts -> problem
        if len(split_node_text) % 2 == 0:
            raise Exception("Error: delimiters not properly closed.")

        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            for idx, part in enumerate(split_node_text):
                if idx % 2 == 0:
                    # first part is always plain text, even if empty
                    new_nodes.append(
                        TextNode(
                            part,
                            TextType.PLAIN,
                        )
                    )
                else:
                    new_nodes.append(
                        TextNode(
                            part,
                            text_type,
                        )
                    )

    return new_nodes


def extract_markdown_images(text):
    regex = r"\!\[(.*?)\]\((.*?)\)"
    results = findall(regex, text)
    return results


def extract_markdown_links(text):
    regex = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    results = findall(regex, text)
    return results


def split_nodes_link(old_nodes):
    return split_nodes_hypertext(old_nodes, "link")


def split_nodes_image(old_nodes):
    return split_nodes_hypertext(old_nodes, "image")


def split_nodes_hypertext(old_nodes, kind):
    '''
    Take an input list of nodes and split each one of them into new nodes, defined by the given hypertext markdown syntax.
    '''

    match kind:
        case "link":
            full_regex = r"(?<!\!)(\[.*?\]\(.*?\))"
            parts_regex = r"(?<!\!)\[(.*?)\]\((.*?)\)"
            text_type = TextType.LINK

        case "image":
            full_regex = r"(\!\[.*?\]\(.*?\))"
            parts_regex = r"\!\[(.*?)\]\((.*?)\)"
            text_type = TextType.IMAGE

    new_nodes = []
    for node in old_nodes:

        split_text = split(
            full_regex,
            node.text,
        )

        for text_part in split_text:
            hypertext_parts = match(parts_regex, text_part)
            if hypertext_parts:
                new_nodes.append(
                    TextNode(
                        hypertext_parts.group(1),
                        text_type,
                        hypertext_parts.group(2),
                    )
                )
            else:
                new_nodes.append(
                    TextNode(
                        text_part,
                        node.text_type,
                        node.url,
                    )
                )

        to_delete = []
        for idx, node in enumerate(new_nodes):
            if not node.text:
                to_delete.append(idx)
        for idx in to_delete[::-1]:
            del new_nodes[idx]

    return new_nodes


