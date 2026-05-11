from textwrap import dedent
import unittest

from markdown_block_functions import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_simple_case(self):

        md = dedent("""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """)

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_normal_paragraph(self):
        block = "This is just a normal paragraph."

        block_type = BlockType.PARAGRAPH

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_heading_1(self):
        block = "# This is a first level heading."

        block_type = BlockType.HEADING

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_heading_2(self):
        block = "## This is a second level heading."

        block_type = BlockType.HEADING

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_code(self):
        block = dedent("""\
            ```
            for file in *; do
                echo "$file"
            done
            ```
        """)

        block_type = BlockType.CODE

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_quote(self):
        block = dedent("""
            > Beautiful quote from a random book.
            >Another one.
        """).strip()

        block_type = BlockType.QUOTE

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_quote_fail(self):
        block = dedent("""
            > Beautiful quote from a random book.
            Oops.
        """).strip()

        block_type = BlockType.QUOTE

        self.assertNotEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_unordered_list(self):
        block = dedent("""
            - First item of a very interesting list.
            - Second item.
        """).strip()

        block_type = BlockType.UNORDERED_LIST

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_unordered_list_fail(self):
        block = dedent("""
            - First item of a very interesting list.
            Oops.
        """).strip()

        block_type = BlockType.PARAGRAPH

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_ordered_list_one_item(self):
        block = dedent("""
            1. First item of a very interesting list.
        """).strip()

        block_type = BlockType.ORDERED_LIST

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_ordered_list_multiple_items(self):
        block = dedent("""
            1. First item of a very interesting list.
            2. Second item of a very interesting list.
            3. Third item of a very interesting list.
        """).strip()

        block_type = BlockType.ORDERED_LIST

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_ordered_list_multiple_items_out_of_order(self):
        block = dedent("""
            1. First item of a very interesting list.
            3. Second item of a very interesting list.
            2. Third item of a very interesting list.
        """).strip()

        block_type = BlockType.PARAGRAPH

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_ordered_list_multiple_items_random_start(self):
        block = dedent("""
            4. First item of a very interesting list.
            5. Second item of a very interesting list.
            6. Third item of a very interesting list.
        """).strip()

        block_type = BlockType.ORDERED_LIST

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )

    def test_ordered_list_false(self):
        block = dedent("""
            First item of a malformed interesting list.
            5. Second item of a very interesting list.
            6. Third item of a very interesting list.
        """).strip()

        block_type = BlockType.PARAGRAPH

        self.assertEqual(
            block_to_block_type(block),
            block_type,
        )


if __name__ == "__main__":
    unittest.main()

