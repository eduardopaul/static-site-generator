from re import findall

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

