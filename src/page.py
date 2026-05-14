from pathlib import Path
from re import match, sub

from copy_contents import copy_contents
from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    try:
        title = match(r"\s*# *(.+)", markdown).group(1)
    except AttributeError:
        title = ""

    return title.strip()

def generate_page(
    from_path: Path,
    template_path: Path,
    dest_path: Path,
    static_path: Path = Path("static"),
    public_path: Path = Path("public"),
):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    copy_contents(static_path, public_path)

    with open(from_path, "r") as file:
        md = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html = sub(
        "{{ Title }}",
        extract_title(md),
        template,
    )

    html = sub(
        "{{ Content }}",
        markdown_to_html_node(md).to_html(),
        html,
    )

    with open(dest_path, "w") as html_file:
        html_file.write(html)

