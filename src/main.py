from pathlib import Path
from sys import argv

from copy_contents import copy_contents
from page import generate_pages_recursive


def main():
    try:
        basepath = argv[1]
    except IndexError:
        basepath = "/"

    copy_contents(
        Path("static"),
        Path("docs"),
    )

    generate_pages_recursive(
        Path("content"),
        Path("template.html"),
        Path("docs"),
        basepath,
    )

main()

