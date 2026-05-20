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
    base_path: str = "/",
):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

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

    html = sub(
        'href="/',
        f'href="{base_path}',
        html,
    )

    html = sub(
        'src="/',
        f'src="{base_path}',
        html,
    )

    with open(dest_path, "w") as html_file:
        html_file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"):
    for path in dir_path_content.iterdir():
        if path.is_dir():
            new_dest_dir_path = dest_dir_path/path.name
            new_dest_dir_path.mkdir()
            generate_pages_recursive(path, template_path, dest_dir_path/path.name, base_path)
        else:
            new_dest_dir_path = dest_dir_path/path.name.replace("md", "html")
            generate_page(path, template_path, new_dest_dir_path, base_path)

