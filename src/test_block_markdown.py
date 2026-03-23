import unittest
from block_markdown import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()