from pathlib import Path


def rmtree(path):
    for item in path.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            rmtree(item)
            item.rmdir()

def cptree(src, dst):
    if not dst.is_dir():
        dst.mkdir()
    for item in src.iterdir():
        item_rel = item.relative_to(src)
        if item.is_file():
            item.copy(dst/item_rel)
        elif item.is_dir():
            (dst/item_rel).mkdir()
            cptree(src/item_rel, dst/item_rel)

def copy_contents(
    src: Path = Path("static"),
    dst: Path = Path("public"),
):
    if dst.is_dir():
        rmtree(dst)
    cptree(src, dst)

