from pathlib import Path


def rmtree(path):
    for item in path.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            rmtree(item)
            item.rmdir()

def cptree(src, dst):
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
    rmtree(dst)
    cptree(src, dst)

