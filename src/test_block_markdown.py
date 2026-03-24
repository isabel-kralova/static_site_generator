import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_strip_whitespace(self):
        md = "   This is block one   \n\n   This is block two   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is block one",
                "This is block two",
            ],
        )

    def test_remove_empty_blocks(self):
        md = "Block one\n\n\n\nBlock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block one",
                "Block two",
            ],
        )
    
class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
    
    def test_code(self):
        code = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote(self):
        quote = "> This is a quote\n> spread over several lines"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        bad_quote = "> First line ok\nsecond no"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ul = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)
        bad_ol = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)
        bad_ol_start = "2. First"
        self.assertEqual(block_to_block_type(bad_ol_start), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("###Nospace"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()