from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
import unittest
from unittest.mock import patch

from copy_contents import copy_contents
from page import generate_page


class TestGeneratePage(unittest.TestCase):

    def setUp(self):
        self.path_ = TemporaryDirectory()
        self.path = Path(self.path_.name)

        self.static_path = self.path / "static"
        self.public_path = self.path / "public"
        self.from_path = self.path / "content/index.md"
        self.dest_path = self.path / "public/index.html"

        self.static_path.mkdir()
        self.public_path.mkdir()
        (self.path / "static/images").mkdir()
        (self.path / "content").mkdir()

        (self.path / "static/images/image.jpg").touch()
        (self.path / "static/index.css").touch()
        self.from_path.touch()

        # We use the original template. There's no need for the temp directory.
        self.template_path = "template.html"

    def test_print(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            generate_page(self.from_path, self.template_path, self.dest_path, self.static_path, self.public_path)

            self.assertEqual(
                mock_stdout.getvalue(),
                f"Generating page from {self.from_path} to {self.dest_path} using {self.template_path}\n",
            )

    def test_copy_static(self):
        static_tree = {
            p.relative_to(self.static_path)
            for p in self.static_path.glob("**/*")
        }

        # Just to silence printing.
        with patch("builtins.print"):
            generate_page(self.from_path, self.template_path, self.dest_path, self.static_path, self.public_path)

        public_tree = {
            p.relative_to(self.public_path)
            for p in self.public_path.glob("**/*")
        }
        public_tree.discard(Path("index.html"))

        self.assertEqual(
            static_tree,
            public_tree,
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
            generate_page(self.from_path, self.template_path, self.dest_path, self.static_path, self.public_path)

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

        try:
            html_output = self.dest_path.read_text()
        except OSError:
            html_output = ""

        self.assertEqual(
            html_output,
            template,
        )

    def tearDown(self):
        self.path_.cleanup()


if __name__ == "__main__":
    unittest.main()

