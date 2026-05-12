from pathlib import Path

from copy_contents import copy_contents


def main():
    copy_contents(Path("./static"), Path("./public"))

main()

