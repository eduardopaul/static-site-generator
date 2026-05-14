from pathlib import Path

from page import generate_page


def main():
    generate_page(
        Path("content/index.md"),
        Path("template.html"),
        Path("public/index.html"),
    )

main()

