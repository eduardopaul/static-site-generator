from pathlib import Path

from copy_contents import copy_contents
from page import generate_pages_recursive


def main():
    copy_contents()
    generate_pages_recursive(
        Path("content"),
        Path("template.html"),
        Path("public"),
    )

main()

