from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from copy_contents import copy_contents


class TestCopyContents(unittest.TestCase):

    def setUp(self):
        self.src = TemporaryDirectory()
        self.src_path = Path(self.src.name)

        self.dst = TemporaryDirectory()
        self.dst_path = Path(self.dst.name)

    def test_clean_public(self):
        (self.dst_path / "outer_file").touch()
        (self.dst_path / "dir").mkdir()
        (self.dst_path / "dir/inner_file").touch()
        (self.dst_path / "dir/inner_dir").mkdir()
        (self.dst_path / "dir/inner_dir/inner_file2").touch()

        copy_contents(self.src_path, self.dst_path)

        # From the docs:
        # Changed in version 3.13: Globbing with a pattern that ends with “**” returns both files and directories. In previous versions, only directories were returned.
        dst_tree = set(self.dst_path.glob("**/*"))

        self.assertEqual(
            # The `glob` method includes the directory itself.
            len(dst_tree),
            0,
        )

    def test_copy_contents(self):
        (self.src_path / "dir").mkdir()
        (self.src_path / "outer_file").touch()
        (self.src_path / "dir/inner_file").touch()
        (self.src_path / "dir/inner_dir").mkdir()
        (self.src_path / "dir/inner_dir/inner_file2").touch()

        src_tree = {
            p.relative_to(self.src_path)
            for p in self.src_path.glob("**/*")
        }
        src_tree.discard(self.src_path)

        copy_contents(self.src_path, self.dst_path)

        dst_tree = {
            p.relative_to(self.dst_path)
            for p in self.dst_path.glob("**/*")
        }
        dst_tree.discard(self.dst_path)

        self.assertEqual(
            src_tree,
            dst_tree,
        )

    def tearDown(self):
        self.src.cleanup()
        self.dst.cleanup()


if __name__ == "__main__":
    unittest.main()

