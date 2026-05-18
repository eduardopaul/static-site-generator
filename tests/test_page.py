from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
import unittest
from unittest.mock import patch

from copy_contents import copy_contents
from page import generate_page, generate_pages_recursive


class TestGeneratePage(unittest.TestCase):

    def setUp(self):
        self.path_ = TemporaryDirectory()
        self.path = Path(self.path_.name)

        (self.path / "content").mkdir()
        (self.path / "public").mkdir()

        self.from_path = self.path / "content/index.md"
        self.from_path.touch()

        self.dest_path = self.path / "public/index.html"
        self.dest_path.touch()

        # We use the original template. There's no need for the temp directory.
        self.template_path = "template.html"

    def test_print(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            generate_page(self.from_path, self.template_path, self.dest_path)

            self.assertEqual(
                mock_stdout.getvalue(),
                f"Generating page from {self.from_path} to {self.dest_path} using {self.template_path}\n",
            )

    def test_generate_page(self):
        self.from_path.write_text(
            dedent(
                """\
                 # Main title

                 Paragraph.

                 - one
                 - two
                 - three"""
            )
        )

        with patch("builtins.print"):
            generate_page(self.from_path, self.template_path, self.dest_path)

        template = dedent(
            """\
            <!doctype html>
            <html>
              <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>Main title</title>
                <link href="/index.css" rel="stylesheet" />
              </head>

              <body>
                <article><div><h1>Main title</h1><p>Paragraph.</p><ul><li>one</li><li>two</li><li>three</li></ul></div></article>
              </body>
            </html>\n"""
        )

        html_output = self.dest_path.read_text()

        self.assertEqual(
            html_output,
            template,
        )

    def tearDown(self):
        self.path_.cleanup()


class TestGeneratePageRecursive(unittest.TestCase):
    def setUp(self):
        self.root_path = TemporaryDirectory()

        self.content_path = Path(self.root_path.name) / "content"
        self.content_path.mkdir()

        self.public_path = Path(self.root_path.name) / "public"
        self.public_path.mkdir()

    def test_generate_create_files(self):
        (self.content_path / "file0.md").touch()
        (self.content_path / "dir1").mkdir()
        (self.content_path / "dir1/file1.md").touch()
        (self.content_path / "dir1/dir2").mkdir()
        (self.content_path / "dir1/dir2/file2.md").touch()

        with patch("builtins.print"):
            generate_pages_recursive(self.content_path, Path("template.html"), self.public_path)

        expected_tree = {
            Path("file0.html"),
            Path("dir1"),
            Path("dir1/file1.html"),
            Path("dir1/dir2"),
            Path("dir1/dir2/file2.html"),
        }

        public_tree = {
            p.relative_to(self.public_path)
            for p in self.public_path.glob("**/*")
        }

        self.assertEqual(
            expected_tree,
            public_tree,
        )

    def test_generate_pages(self):
        markdown_file = self.content_path / "markdown_file.md"
        markdown_file.touch()
        markdown_file.write_text(dedent(
            """\
            # Heading

            text

            - list 1
            - list **2**"""
        ))

        with patch("builtins.print"):
            generate_pages_recursive(self.content_path, Path("template.html"), self.public_path)

        expected_html = dedent(
            """\
            <!doctype html>
            <html>
              <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>Heading</title>
                <link href="/index.css" rel="stylesheet" />
              </head>

              <body>
                <article><div><h1>Heading</h1><p>text</p><ul><li>list 1</li><li>list <b>2</b></li></ul></div></article>
              </body>
            </html>\n"""
        )

        self.assertEqual(
            expected_html,
            (self.public_path / "markdown_file.html").read_text(),
        )

    def tearDown(self):
        self.root_path.cleanup()


if __name__ == "__main__":
    unittest.main()

